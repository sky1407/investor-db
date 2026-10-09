import json
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel

from investordb.models import (
    CheckResult,
    CheckStatus,
    EntityKind,
    Evidence,
    ExclusionReason,
    Investment,
    MoneyFact,
    ResearchRecord,
)

ACTIVITY_MONTHS = 36
KIND_EXCLUSIONS: dict[EntityKind, ExclusionReason] = {
    "service_provider": "not_investor_service",
    "lender": "debt_only",
    "platform": "platform_only",
    "grant_scheme": "grant_only",
    "public_markets_manager": "public_markets_only",
}


class FxRates(BaseModel):
    base: Literal["EUR"]
    rate_date: date
    source_url: str
    rates: dict[str, float]

    @classmethod
    def load(cls, path: Path) -> "FxRates":
        return cls.model_validate(json.loads(path.read_text(encoding="utf-8")))

    def to_eur(self, amount: float, currency: str) -> int:
        rate = self.rates.get(currency)
        if rate is None or rate <= 0:
            raise ValueError(f"missing FX rate for {currency}")
        return round(amount / rate)


class FieldOut(BaseModel):
    value: str | int | list[str] | None
    source_url: str
    source_date: date | None
    quote: str
    status: CheckStatus
    original_amount: float | None = None
    original_currency: str | None = None


class InvestmentOut(BaseModel):
    company: str
    deal_date: date
    in_window: bool
    source_url: str
    source_date: date | None
    quote: str
    status: CheckStatus


class InvestorOut(BaseModel):
    candidate_id: str
    name: str
    country: str
    active_in: list[str]
    website: str | None
    funds: list[str]
    included: bool
    exclusion_reason: ExclusionReason | None
    confidence: Literal["high", "medium"] | None
    needs_review: bool
    issues: list[str]
    entity_kind: FieldOut
    investor_type: FieldOut | None
    sectors: FieldOut | None
    stages: FieldOut | None
    ticket_min_eur: FieldOut | None
    ticket_max_eur: FieldOut | None
    aum_eur: FieldOut | None
    investments: list[InvestmentOut]
    last_evidence_date: date | None
    notes: str


def window_start(as_of: date, months: int = ACTIVITY_MONTHS) -> date:
    total = as_of.year * 12 + as_of.month - 1 - months
    year, month = divmod(total, 12)
    month += 1
    for day in (as_of.day, 30, 29, 28):
        try:
            return date(year, month, day)
        except ValueError:
            continue
    raise ValueError("unreachable")


def _status(checks: dict[str, CheckResult], name: str) -> CheckStatus:
    check = checks.get(name)
    return check.status if check else "fetch_error"


def _field(evidence: Evidence, status: CheckStatus, value: str | int | list[str] | None) -> FieldOut:
    return FieldOut(
        value=value if status == "verified" else None,
        source_url=str(evidence.source_url),
        source_date=evidence.source_date,
        quote=evidence.quote,
        status=status,
    )


def _money(fact: MoneyFact | None, status: CheckStatus, fx: FxRates) -> FieldOut | None:
    if fact is None:
        return None
    out = _field(fact, status, fx.to_eur(fact.amount, fact.currency))
    return out.model_copy(update={"original_amount": fact.amount, "original_currency": fact.currency})


def _investment(inv: Investment, status: CheckStatus, start: date, as_of: date) -> InvestmentOut:
    return InvestmentOut(
        company=inv.company,
        deal_date=inv.deal_date,
        in_window=start <= inv.deal_date <= as_of,
        source_url=str(inv.source_url),
        source_date=inv.source_date,
        quote=inv.quote,
        status=status,
    )


def decide(
    record: ResearchRecord,
    investments: list[InvestmentOut],
    kind_status: CheckStatus,
    type_status: CheckStatus | None,
) -> tuple[ExclusionReason | None, Literal["high", "medium"] | None]:
    if record.duplicate_of:
        return "duplicate", None
    kind = record.entity_kind.value
    if kind != "investor":
        return KIND_EXCLUSIONS[kind], None
    verified = [i for i in investments if i.status == "verified"]
    if not verified:
        return "no_evidence", None
    recent = [i for i in verified if i.in_window]
    if not recent:
        return "inactive", None
    strategy_proven = kind_status == "verified" or type_status == "verified"
    if not strategy_proven and len(verified) < 2:
        return "no_evidence", None
    if kind_status == "verified" and type_status == "verified" and len(recent) >= 2:
        return None, "high"
    return None, "medium"


def build_record(
    record: ResearchRecord, checks: dict[str, CheckResult], fx: FxRates, as_of: date
) -> InvestorOut:
    start = window_start(as_of)
    investments = sorted(
        (
            _investment(inv, _status(checks, f"investments[{i}]"), start, as_of)
            for i, inv in enumerate(record.investments)
        ),
        key=lambda inv: inv.deal_date,
        reverse=True,
    )
    kind_status = _status(checks, "entity_kind")
    type_status = _status(checks, "investor_type") if record.investor_type else None
    reason, confidence = decide(record, investments, kind_status, type_status)

    fields = {
        "investor_type": (record.investor_type, lambda f: f.value),
        "sectors": (record.sectors, lambda f: f.value),
        "stages": (record.stages, lambda f: list(f.value)),
    }
    built = {
        name: _field(fact, _status(checks, name), getter(fact)) if fact else None
        for name, (fact, getter) in fields.items()
    }
    ticket_min = _money(record.ticket_min, _status(checks, "ticket_min"), fx)
    ticket_max = _money(record.ticket_max, _status(checks, "ticket_max"), fx)
    aum = _money(record.aum, _status(checks, "aum"), fx)

    issues = [f"{name}: {check.status}" for name, check in checks.items() if check.status != "verified"]
    if (
        ticket_min
        and ticket_max
        and ticket_min.value is not None
        and ticket_max.value is not None
        and ticket_min.value > ticket_max.value
    ):
        issues.append("ticket_min_eur > ticket_max_eur")
    future = [i.company for i in investments if i.deal_date > as_of]
    if future:
        issues.append(f"deal_date in the future: {', '.join(future)}")

    verified_dates = [i.deal_date for i in investments if i.status == "verified" and i.deal_date <= as_of]
    return InvestorOut(
        candidate_id=record.candidate_id,
        name=record.name,
        country=record.country,
        active_in=record.active_in,
        website=str(record.website) if record.website else None,
        funds=record.funds,
        included=reason is None,
        exclusion_reason=reason,
        confidence=confidence,
        needs_review=bool(issues),
        issues=issues,
        entity_kind=_field(record.entity_kind, kind_status, record.entity_kind.value),
        investor_type=built["investor_type"],
        sectors=built["sectors"],
        stages=built["stages"],
        ticket_min_eur=ticket_min,
        ticket_max_eur=ticket_max,
        aum_eur=aum,
        investments=investments,
        last_evidence_date=max(verified_dates, default=None),
        notes=record.notes,
    )
