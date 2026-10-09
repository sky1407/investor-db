from datetime import date

import pytest

from investordb.build import FxRates, build_record, window_start
from investordb.io import DATA_DIR
from investordb.models import CheckResult, ResearchRecord
from tests.test_models import base_record

AS_OF = date(2026, 10, 9)
FX = FxRates(base="EUR", rate_date=date(2026, 10, 8), source_url="https://ecb", rates={"EUR": 1, "CZK": 25})


def inv(company, deal_date, url="https://example.com/deal"):
    return {"company": company, "deal_date": deal_date, "source_url": url, "quote": f"invested in {company}"}


def checks_for(record, overrides=None):
    overrides = overrides or {}
    return {
        name: CheckResult(url=str(ev.source_url), status=overrides.get(name, "verified"))
        for name, ev in record.evidence_items()
    }


def build(overrides=None, **record_fields):
    record = ResearchRecord.model_validate(base_record(**record_fields))
    return build_record(record, checks_for(record, overrides), FX, AS_OF)


@pytest.mark.parametrize(
    ("as_of", "expected"),
    [
        (date(2026, 10, 9), date(2023, 10, 9)),
        (date(2026, 1, 15), date(2023, 1, 15)),
        (date(2028, 2, 29), date(2025, 2, 28)),
        (date(2026, 3, 31), date(2023, 3, 31)),
    ],
)
def test_window_start(as_of, expected):
    assert window_start(as_of) == expected


def test_verified_investor_with_two_recent_deals_is_high_confidence():
    out = build(investments=[inv("A", "2025-01-01"), inv("B", "2024-06-01")])
    assert out.included
    assert out.confidence == "high"
    assert out.last_evidence_date == date(2025, 1, 1)
    assert [i.company for i in out.investments] == ["A", "B"]


def test_single_recent_deal_is_medium_confidence():
    out = build()
    assert out.included
    assert out.confidence == "medium"


def test_deal_exactly_at_window_start_counts():
    assert build(investments=[inv("A", "2023-10-09")]).included


def test_only_old_deals_means_inactive():
    out = build(investments=[inv("A", "2023-10-08")])
    assert not out.included
    assert out.exclusion_reason == "inactive"


def test_unverified_deal_is_not_evidence():
    out = build(overrides={"investments[0]": "quote_not_found"})
    assert out.exclusion_reason == "no_evidence"
    assert out.needs_review
    assert "investments[0]: quote_not_found" in out.issues


def test_no_investments_means_no_evidence():
    assert build(investments=[]).exclusion_reason == "no_evidence"


def test_strategy_or_two_deals_required():
    one_deal = build(overrides={"entity_kind": "http_error", "investor_type": "quote_not_found"})
    assert one_deal.exclusion_reason == "no_evidence"
    two_deals = build(
        overrides={"entity_kind": "http_error", "investor_type": "quote_not_found"},
        investments=[inv("A", "2025-01-01"), inv("B", "2024-01-01")],
    )
    assert two_deals.included
    assert two_deals.confidence == "medium"


@pytest.mark.parametrize(
    ("kind", "reason"),
    [
        ("service_provider", "not_investor_service"),
        ("lender", "debt_only"),
        ("platform", "platform_only"),
        ("grant_scheme", "grant_only"),
        ("public_markets_manager", "public_markets_only"),
    ],
)
def test_non_investors_are_excluded(kind, reason):
    entity = {"value": kind, "source_url": "https://neulogy.vc/", "quote": "We provide services"}
    out = build(entity_kind=entity, investor_type=None)
    assert out.exclusion_reason == reason
    assert out.confidence is None


def test_duplicate_wins_over_everything():
    assert build(duplicate_of="c001").exclusion_reason == "duplicate"


def test_unverified_field_value_is_hidden_but_source_kept():
    sectors = {"value": ["fintech"], "source_url": "https://neulogy.vc/s", "quote": "we love fintech"}
    out = build(sectors=sectors, overrides={"sectors": "quote_not_found"})
    assert out.sectors.value is None
    assert out.sectors.quote == "we love fintech"
    assert out.included


def test_money_is_converted_to_eur():
    money = {
        "amount": 50_000_000,
        "currency": "CZK",
        "source_url": "https://neulogy.vc/",
        "quote": "50 mil. Kč",
    }
    out = build(aum=money)
    assert out.aum_eur.value == 2_000_000
    assert out.aum_eur.original_currency == "CZK"


def test_ticket_range_inconsistency_is_flagged():
    low = {
        "amount": 3_000_000,
        "currency": "EUR",
        "source_url": "https://neulogy.vc/",
        "quote": "minimum 3 mil. EUR",
    }
    high = {
        "amount": 500_000,
        "currency": "EUR",
        "source_url": "https://neulogy.vc/",
        "quote": "maximum 500 tis. EUR",
    }
    out = build(ticket_min=low, ticket_max=high)
    assert "ticket_min_eur > ticket_max_eur" in out.issues


def test_future_deal_is_flagged_and_not_in_window():
    out = build(investments=[inv("A", "2027-01-01")])
    assert out.exclusion_reason == "inactive"
    assert any("future" in issue for issue in out.issues)


def test_missing_fx_rate_raises():
    with pytest.raises(ValueError, match="missing FX rate"):
        FX.to_eur(1, "PLN")


def test_committed_fx_file_loads():
    fx = FxRates.load(DATA_DIR / "fx_rates.json")
    assert fx.to_eur(fx.rates["CZK"], "CZK") == 1
