import pytest
from pydantic import ValidationError

from investordb.models import ResearchRecord


def base_record(**overrides):
    record = {
        "candidate_id": "c009",
        "name": "Neulogy Ventures",
        "country": "SK",
        "entity_kind": {
            "value": "investor",
            "source_url": "https://neulogy.vc/",
            "quote": "We invest in early stage technology companies",
        },
        "investor_type": {
            "value": "vc",
            "source_url": "https://neulogy.vc/",
            "quote": "We invest in early stage technology companies",
        },
        "investments": [
            {
                "company": "Acme",
                "deal_date": "2025-03-01",
                "source_url": "https://example.com/acme",
                "quote": "Neulogy Ventures invested in Acme",
            }
        ],
        "researched_at": "2026-10-09",
    }
    record.update(overrides)
    return record


def test_valid_record_parses():
    record = ResearchRecord.model_validate(base_record())
    assert record.investor_type.value == "vc"
    assert record.investments[0].deal_date.isoformat() == "2025-03-01"


def test_investor_without_type_is_rejected():
    with pytest.raises(ValidationError, match="requires investor_type"):
        ResearchRecord.model_validate(base_record(investor_type=None))


def test_service_provider_without_type_is_allowed():
    kind = {
        "value": "service_provider",
        "source_url": "https://law.sk/",
        "quote": "Law firm and tax advisory",
    }
    record = ResearchRecord.model_validate(base_record(entity_kind=kind, investor_type=None, investments=[]))
    assert record.entity_kind.value == "service_provider"


def test_unknown_fields_are_rejected():
    with pytest.raises(ValidationError):
        ResearchRecord.model_validate(base_record(confidence="high"))


@pytest.mark.parametrize("quote", ["", "       ", "short"])
def test_quote_must_have_content(quote):
    kind = {"value": "investor", "source_url": "https://neulogy.vc/", "quote": quote}
    with pytest.raises(ValidationError):
        ResearchRecord.model_validate(base_record(entity_kind=kind))


def test_negative_amount_is_rejected():
    aum = {
        "amount": -5,
        "currency": "EUR",
        "source_url": "https://neulogy.vc/",
        "quote": "fund size of 5 mil",
    }
    with pytest.raises(ValidationError):
        ResearchRecord.model_validate(base_record(aum=aum))


def test_unknown_stage_is_rejected():
    stages = {"value": ["series-z"], "source_url": "https://neulogy.vc/", "quote": "we invest in all stages"}
    with pytest.raises(ValidationError):
        ResearchRecord.model_validate(base_record(stages=stages))


def test_self_duplicate_is_rejected():
    with pytest.raises(ValidationError, match="duplicate of itself"):
        ResearchRecord.model_validate(base_record(duplicate_of="c009"))


def test_invalid_active_in_code_is_rejected():
    with pytest.raises(ValidationError, match="invalid country code"):
        ResearchRecord.model_validate(base_record(active_in=["svk"]))


def test_evidence_items_lists_every_fact():
    record = ResearchRecord.model_validate(base_record())
    assert [name for name, _ in record.evidence_items()] == ["entity_kind", "investor_type", "investments[0]"]
