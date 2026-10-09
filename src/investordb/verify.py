from collections import Counter
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from typing import Protocol

from investordb.fetch import DEFAULT_LANGUAGE, FALLBACK_LANGUAGE, FetchError, Page
from investordb.models import CheckResult, Evidence, ResearchRecord
from investordb.textnorm import contains_quote

VerifyReport = dict[str, dict[str, CheckResult]]


class Fetcher(Protocol):
    def get(self, url: str, language: str = DEFAULT_LANGUAGE) -> Page: ...


def check_evidence(evidence: Evidence, page: Page | FetchError) -> CheckResult:
    url = str(evidence.source_url)
    if isinstance(page, FetchError):
        return CheckResult(url=url, status="fetch_error", detail=str(page)[:300])
    if page.status >= 400:
        return CheckResult(url=url, status="http_error", http_status=page.status)
    if not page.text:
        return CheckResult(
            url=url, status="unsupported_content", http_status=page.status, detail=page.content_type
        )
    if contains_quote(page.text, evidence.quote):
        return CheckResult(url=url, status="verified", http_status=page.status)
    return CheckResult(url=url, status="quote_not_found", http_status=page.status)


def _safe_get(fetcher: Fetcher, url: str, language: str = DEFAULT_LANGUAGE) -> Page | FetchError:
    try:
        return fetcher.get(url, language)
    except FetchError as exc:
        return exc


def verify_records(records: Iterable[ResearchRecord], fetcher: Fetcher, workers: int = 8) -> VerifyReport:
    records = list(records)
    urls = sorted({str(ev.source_url) for r in records for _, ev in r.evidence_items()})
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        pages = dict(zip(urls, pool.map(lambda u: _safe_get(fetcher, u), urls), strict=True))
        report = {
            r.candidate_id: {
                name: check_evidence(ev, pages[str(ev.source_url)]) for name, ev in r.evidence_items()
            }
            for r in records
        }
        retry = sorted(
            {
                check.url
                for checks in report.values()
                for check in checks.values()
                if check.status == "quote_not_found"
            }
        )
        fallback = dict(
            zip(retry, pool.map(lambda u: _safe_get(fetcher, u, FALLBACK_LANGUAGE), retry), strict=True)
        )
    for record in records:
        checks = report[record.candidate_id]
        for name, ev in record.evidence_items():
            if checks[name].status == "quote_not_found":
                second = check_evidence(ev, fallback[str(ev.source_url)])
                if second.status == "verified":
                    checks[name] = second.model_copy(
                        update={"detail": f"matched with Accept-Language: {FALLBACK_LANGUAGE}"}
                    )
    return report


def summarize(report: VerifyReport) -> dict[str, int]:
    counts = Counter(check.status for checks in report.values() for check in checks.values())
    return dict(sorted(counts.items()))
