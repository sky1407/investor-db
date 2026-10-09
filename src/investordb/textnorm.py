import re
import unicodedata
from html.parser import HTMLParser

_SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}
_BLOCK_TAGS = {
    "p",
    "div",
    "br",
    "li",
    "ul",
    "ol",
    "tr",
    "td",
    "th",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "section",
    "article",
    "header",
    "footer",
    "blockquote",
    "table",
    "dd",
    "dt",
}
_META_NAMES = {"description", "og:description", "og:title", "twitter:description"}
_SINGLE_QUOTES = (0x2018, 0x2019, 0x201A, 0x201B, 0x2032)
_DOUBLE_QUOTES = (0x201C, 0x201D, 0x201E, 0x201F, 0x00AB, 0x00BB)
_DASHES = (0x2013, 0x2014, 0x2011, 0x2012, 0x2212)
_SPACES = (0x00A0, 0x202F, 0x2009)
_INVISIBLE = (0x00AD, 0x200B, 0x200C, 0x200D, 0xFEFF)
_TRANSLATE = str.maketrans(
    {
        **dict.fromkeys(_SINGLE_QUOTES, "'"),
        **dict.fromkeys(_DOUBLE_QUOTES, '"'),
        **dict.fromkeys(_DASHES, "-"),
        **dict.fromkeys(_SPACES, " "),
        **dict.fromkeys(_INVISIBLE, None),
        0x2026: "...",
    }
)
_WS = re.compile(r"\s+")


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
        elif tag == "meta":
            values = dict(attrs)
            key = (values.get("name") or values.get("property") or "").lower()
            if key in _META_NAMES and values.get("content"):
                self.parts.append(f"\n{values['content']}\n")
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    parser = _TextExtractor()
    parser.feed(html)
    parser.close()
    return "".join(parser.parts)


def normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.translate(_TRANSLATE))
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return _WS.sub(" ", stripped.casefold()).strip()


def contains_quote(page_text: str, quote: str) -> bool:
    needle = normalize(quote)
    return bool(needle) and needle in normalize(page_text)
