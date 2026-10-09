import csv
from pathlib import Path

from investordb.build import FieldOut, InvestorOut

INCLUDED_COLUMNS = [
    "candidate_id",
    "name",
    "country",
    "active_in",
    "website",
    "investor_type",
    "investor_type_source",
    "sectors",
    "sectors_source",
    "stages",
    "stages_source",
    "ticket_min_eur",
    "ticket_min_source",
    "ticket_max_eur",
    "ticket_max_source",
    "aum_eur",
    "aum_source",
    "latest_investment",
    "latest_investment_date",
    "latest_investment_source",
    "verified_investments",
    "confidence",
    "needs_review",
]
EXCLUDED_COLUMNS = [
    "candidate_id",
    "name",
    "country",
    "exclusion_reason",
    "entity_kind",
    "entity_kind_source",
    "entity_kind_quote",
    "needs_review",
    "notes",
]


def _value(field: FieldOut | None) -> str:
    if field is None or field.value is None:
        return ""
    if isinstance(field.value, list):
        return "; ".join(field.value)
    return str(field.value)


def _source(field: FieldOut | None) -> str:
    if field is None or field.value is None:
        return ""
    return f"{field.source_url} ({field.source_date})" if field.source_date else field.source_url


def included_row(out: InvestorOut) -> dict[str, str]:
    verified = [i for i in out.investments if i.status == "verified"]
    latest = verified[0] if verified else None
    return {
        "candidate_id": out.candidate_id,
        "name": out.name,
        "country": out.country,
        "active_in": "; ".join(out.active_in),
        "website": out.website or "",
        "investor_type": _value(out.investor_type),
        "investor_type_source": _source(out.investor_type),
        "sectors": _value(out.sectors),
        "sectors_source": _source(out.sectors),
        "stages": _value(out.stages),
        "stages_source": _source(out.stages),
        "ticket_min_eur": _value(out.ticket_min_eur),
        "ticket_min_source": _source(out.ticket_min_eur),
        "ticket_max_eur": _value(out.ticket_max_eur),
        "ticket_max_source": _source(out.ticket_max_eur),
        "aum_eur": _value(out.aum_eur),
        "aum_source": _source(out.aum_eur),
        "latest_investment": latest.company if latest else "",
        "latest_investment_date": latest.deal_date.isoformat() if latest else "",
        "latest_investment_source": latest.source_url if latest else "",
        "verified_investments": str(len(verified)),
        "confidence": out.confidence or "",
        "needs_review": str(out.needs_review).lower(),
    }


def excluded_row(out: InvestorOut) -> dict[str, str]:
    return {
        "candidate_id": out.candidate_id,
        "name": out.name,
        "country": out.country,
        "exclusion_reason": out.exclusion_reason or "",
        "entity_kind": out.entity_kind.value if isinstance(out.entity_kind.value, str) else "",
        "entity_kind_source": out.entity_kind.source_url,
        "entity_kind_quote": out.entity_kind.quote,
        "needs_review": str(out.needs_review).lower(),
        "notes": out.notes,
    }


def write_csv(path: Path, columns: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
