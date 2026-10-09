import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import TracebackType

import httpx

from investordb.textnorm import html_to_text

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
)
DEFAULT_LANGUAGE = "sk,cs;q=0.9,en;q=0.8"
FALLBACK_LANGUAGE = "en"
MAX_BYTES = 8_000_000
HTML_TYPES = {"text/html", "application/xhtml+xml"}
_META_CHARSET = re.compile(rb"""<meta[^>]+charset=["']?([A-Za-z0-9_\-]+)""", re.IGNORECASE)


class FetchError(Exception):
    pass


@dataclass(frozen=True)
class Page:
    url: str
    status: int
    content_type: str
    text: str
    fetched_at: str


def detect_encoding(body: bytes, header_charset: str | None) -> str:
    if header_charset:
        return header_charset
    match = _META_CHARSET.search(body[:4096])
    return match.group(1).decode("ascii") if match else "utf-8"


def decode_body(body: bytes, encoding: str) -> str:
    try:
        return body.decode(encoding, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


class PageFetcher:
    def __init__(
        self,
        cache_dir: Path | None = None,
        client: httpx.Client | None = None,
        timeout: float = 20.0,
    ) -> None:
        self._cache_dir = cache_dir
        self._client = client or httpx.Client(
            follow_redirects=True,
            timeout=timeout,
            headers={"User-Agent": USER_AGENT},
        )

    def __enter__(self) -> "PageFetcher":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self._client.close()

    def get(self, url: str, language: str = DEFAULT_LANGUAGE) -> Page:
        cache_key = url if language == DEFAULT_LANGUAGE else f"{url}|{language}"
        cached = self._read_cache(cache_key)
        if cached is not None:
            return cached
        try:
            with self._client.stream("GET", url, headers={"Accept-Language": language}) as response:
                body = bytearray()
                for chunk in response.iter_bytes():
                    body.extend(chunk)
                    if len(body) > MAX_BYTES:
                        raise FetchError(f"response larger than {MAX_BYTES} bytes")
                status = response.status_code
                content_type = response.headers.get("content-type", "").split(";")[0].strip().lower()
                header_charset = response.charset_encoding
        except httpx.HTTPError as exc:
            raise FetchError(f"{type(exc).__name__}: {exc}") from exc
        text = ""
        if content_type in HTML_TYPES or content_type == "text/plain" or not content_type:
            raw = decode_body(bytes(body), detect_encoding(bytes(body), header_charset))
            text = raw if content_type == "text/plain" else html_to_text(raw)
        page = Page(url, status, content_type, text, datetime.now(UTC).isoformat(timespec="seconds"))
        self._write_cache(cache_key, page)
        return page

    def _cache_path(self, key: str) -> Path | None:
        if self._cache_dir is None:
            return None
        return self._cache_dir / f"{hashlib.sha256(key.encode()).hexdigest()}.json"

    def _read_cache(self, key: str) -> Page | None:
        path = self._cache_path(key)
        if path is None or not path.exists():
            return None
        try:
            return Page(**json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError):
            return None

    def _write_cache(self, key: str, page: Page) -> None:
        path = self._cache_path(key)
        if path is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(asdict(page), ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)
