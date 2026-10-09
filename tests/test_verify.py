import httpx
import pytest

from investordb.fetch import DEFAULT_LANGUAGE, MAX_BYTES, FetchError, PageFetcher, detect_encoding
from investordb.models import ResearchRecord
from investordb.verify import summarize, verify_records
from tests.test_models import base_record

PAGES = {
    "https://neulogy.vc/": (
        200,
        "text/html; charset=utf-8",
        "<p>We invest in early stage technology companies</p>",
    ),
    "https://example.com/acme": (200, "text/html", "<p>Something else entirely</p>"),
    "https://example.com/gone": (404, "text/html", "not found"),
    "https://example.com/report.pdf": (200, "application/pdf", "%PDF-1.4"),
}


def handler(request: httpx.Request) -> httpx.Response:
    url = str(request.url)
    if url == "https://example.com/timeout":
        raise httpx.ConnectTimeout("timed out", request=request)
    status, content_type, body = PAGES[url]
    return httpx.Response(status, headers={"content-type": content_type}, content=body.encode())


def make_fetcher(cache_dir=None, transport_handler=handler):
    return PageFetcher(
        cache_dir=cache_dir, client=httpx.Client(transport=httpx.MockTransport(transport_handler))
    )


def record_with_investment_url(url):
    investment = {
        "company": "Acme",
        "deal_date": "2025-03-01",
        "source_url": url,
        "quote": "invested in Acme",
    }
    return ResearchRecord.model_validate(base_record(investments=[investment]))


def test_verified_and_hallucinated_quotes():
    report = verify_records([ResearchRecord.model_validate(base_record())], make_fetcher())
    checks = report["c009"]
    assert checks["entity_kind"].status == "verified"
    assert checks["investor_type"].status == "verified"
    assert checks["investments[0]"].status == "quote_not_found"


@pytest.mark.parametrize(
    ("url", "status"),
    [
        ("https://example.com/gone", "http_error"),
        ("https://example.com/report.pdf", "unsupported_content"),
        ("https://example.com/timeout", "fetch_error"),
    ],
)
def test_failure_statuses(url, status):
    report = verify_records([record_with_investment_url(url)], make_fetcher())
    assert report["c009"]["investments[0]"].status == status


def test_each_url_is_fetched_once(tmp_path):
    calls = []

    def counting(request):
        calls.append((str(request.url), request.headers["accept-language"]))
        return handler(request)

    verify_records([ResearchRecord.model_validate(base_record())], make_fetcher(transport_handler=counting))
    assert sorted(calls) == [
        ("https://example.com/acme", "en"),
        ("https://example.com/acme", DEFAULT_LANGUAGE),
        ("https://neulogy.vc/", DEFAULT_LANGUAGE),
    ]


def test_cache_avoids_second_request(tmp_path):
    calls = []

    def counting(request):
        calls.append(1)
        return handler(request)

    for _ in range(2):
        make_fetcher(tmp_path, counting).get("https://neulogy.vc/")
    assert len(calls) == 1


def test_oversized_response_raises():
    def huge(request):
        return httpx.Response(200, headers={"content-type": "text/html"}, content=b"x" * (MAX_BYTES + 1))

    with pytest.raises(FetchError, match="larger than"):
        make_fetcher(transport_handler=huge).get("https://example.com/big")


def test_windows_1250_page_is_decoded():
    body = '<meta charset="windows-1250"><p>Rizikový kapitál pre začínajúce firmy</p>'.encode("cp1250")

    def legacy(request):
        return httpx.Response(200, headers={"content-type": "text/html"}, content=body)

    page = make_fetcher(transport_handler=legacy).get("https://example.com/old")
    assert "Rizikový kapitál pre začínajúce firmy" in page.text


def test_detect_encoding_prefers_header():
    assert detect_encoding(b'<meta charset="windows-1250">', "utf-8") == "utf-8"
    assert detect_encoding(b"<p>x</p>", None) == "utf-8"


def test_summarize_counts_statuses():
    report = verify_records([ResearchRecord.model_validate(base_record())], make_fetcher())
    assert summarize(report) == {"quote_not_found": 1, "verified": 2}


def test_quote_in_other_language_version_is_verified():
    def negotiated(request):
        english = request.headers.get("accept-language") == "en"
        body = "<p>We invest in early stage technology companies</p>" if english else "<p>Investujeme</p>"
        return httpx.Response(200, headers={"content-type": "text/html"}, content=body.encode())

    record = ResearchRecord.model_validate(base_record(investments=[]))
    report = verify_records([record], make_fetcher(transport_handler=negotiated))
    assert report["c009"]["entity_kind"].status == "verified"
    assert "Accept-Language" in report["c009"]["entity_kind"].detail


def test_language_variants_are_cached_separately(tmp_path):
    def negotiated(request):
        body = request.headers.get("accept-language", "").encode()
        return httpx.Response(200, headers={"content-type": "text/plain"}, content=body)

    fetcher = make_fetcher(tmp_path, negotiated)
    assert fetcher.get("https://example.com/").text.startswith("sk")
    assert fetcher.get("https://example.com/", "en").text == "en"
