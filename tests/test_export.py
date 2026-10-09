import csv

from investordb.export import INCLUDED_COLUMNS, excluded_row, included_row, write_csv
from tests.test_build import build, inv


def test_included_row_has_source_next_to_each_value():
    sectors = {
        "value": ["fintech", "saas"],
        "source_url": "https://neulogy.vc/s",
        "source_date": "2025-02-01",
        "quote": "fintech and saas companies",
    }
    row = included_row(build(sectors=sectors, investments=[inv("A", "2024-01-01"), inv("B", "2025-05-01")]))
    assert row["sectors"] == "fintech; saas"
    assert row["sectors_source"] == "https://neulogy.vc/s (2025-02-01)"
    assert row["latest_investment"] == "B"
    assert row["verified_investments"] == "2"
    assert set(row) == set(INCLUDED_COLUMNS)


def test_unverified_value_exports_empty_value_and_source():
    sectors = {"value": ["fintech"], "source_url": "https://neulogy.vc/s", "quote": "fintech companies"}
    row = included_row(build(sectors=sectors, overrides={"sectors": "quote_not_found"}))
    assert row["sectors"] == ""
    assert row["sectors_source"] == ""


def test_excluded_row_keeps_reason_and_quote():
    entity = {"value": "service_provider", "source_url": "https://law.sk/", "quote": "advokátska kancelária"}
    row = excluded_row(build(entity_kind=entity, investor_type=None))
    assert row["exclusion_reason"] == "not_investor_service"
    assert row["entity_kind_quote"] == "advokátska kancelária"


def test_write_csv_round_trip(tmp_path):
    path = tmp_path / "out" / "x.csv"
    write_csv(path, ["a", "b"], [{"a": "1", "b": 'č, "q"'}])
    with path.open(encoding="utf-8") as handle:
        assert list(csv.DictReader(handle)) == [{"a": "1", "b": 'č, "q"'}]
