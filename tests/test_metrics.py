from dataclasses import replace

import pytest

from investordb.metrics import (
    CheckRow,
    apply_ai_verdicts,
    check_items,
    compute_metrics,
    load_rows,
    merge,
    save_rows,
)
from tests.test_build import build, inv

SECTORS = {"value": ["fintech"], "source_url": "https://neulogy.vc/s", "quote": "fintech companies"}
LAW = {"value": "service_provider", "source_url": "https://law.sk/", "quote": "advokátska kancelária"}


def sample():
    return [
        build(sectors=SECTORS, investments=[inv("A", "2025-01-01")]),
        build(candidate_id="c010", entity_kind=LAW, investor_type=None),
        build(candidate_id="c011", country="CZ"),
    ]


def test_check_items_cover_decision_and_filled_fields():
    rows = check_items(sample())
    keys = [r.key for r in rows]
    assert ("c009", "inclusion") in keys
    assert ("c009", "sectors") in keys
    assert ("c009", "latest_investment") in keys
    assert ("c010", "inclusion") in keys
    assert not any(cid == "c010" and item != "inclusion" for cid, item in keys)
    decision = next(r for r in rows if r.key == ("c010", "inclusion"))
    assert decision.system_value == "excluded:not_investor_service"


def test_merge_keeps_verdicts_only_when_value_unchanged():
    generated = check_items(sample())
    judged = [replace(r, human_verdict="correct", human_note="ok") for r in generated]
    assert all(r.human_verdict == "correct" for r in merge(generated, judged))
    changed = [replace(r, system_value="other") for r in judged]
    assert all(r.human_verdict == "" for r in merge(generated, changed))


def test_save_and_load_round_trip(tmp_path):
    rows = [replace(r, ai_verdict="incorrect", ai_note='č, "x"') for r in check_items(sample())]
    path = tmp_path / "manual.csv"
    save_rows(path, rows)
    assert load_rows(path) == rows


def test_load_rejects_invalid_verdict(tmp_path):
    path = tmp_path / "manual.csv"
    save_rows(path, check_items(sample()))
    text = path.read_text(encoding="utf-8").replace(
        "c009,inclusion,included,https://neulogy.vc/,,", "c009,inclusion,included,https://neulogy.vc/,maybe,"
    )
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="invalid verdict"):
        load_rows(path)


def test_missing_file_loads_empty(tmp_path):
    assert load_rows(tmp_path / "none.csv") == []


def verdicts(rows, mapping, column):
    return [replace(r, **{column: mapping.get(r.key, "")}) for r in rows]


def test_metrics_precision_scope_and_human_override():
    built = sample()
    rows = check_items(built)
    ai = {r.key: "correct" for r in rows}
    ai[("c009", "sectors")] = "incorrect"
    rows = verdicts(rows, ai, "ai_verdict")
    rows = verdicts(rows, {("c009", "sectors"): "correct", ("c009", "inclusion"): "correct"}, "human_verdict")

    combined = compute_metrics(built, rows)
    assert combined["records_in_scope"] == 2
    assert combined["inclusion_precision"].value == 1.0
    assert combined["exclusion_accuracy"].value == 1.0
    assert combined["field_accuracy"]["sectors"].value == 1.0
    assert combined["fill_rate"]["sectors"].value == 1.0
    assert combined["ai_agrees_with_human"].correct == 1
    assert combined["ai_agrees_with_human"].total == 2

    human = compute_metrics(built, rows, human_only=True)
    assert human["exclusion_accuracy"].total == 0
    assert human["exclusion_accuracy"].value is None
    assert human["human_checked"].correct == 2


def test_incorrect_inclusion_lowers_precision():
    built = sample()
    rows = verdicts(check_items(built), {("c009", "inclusion"): "incorrect"}, "human_verdict")
    assert compute_metrics(built, rows, human_only=True)["inclusion_precision"].value == 0.0


def test_check_row_final_verdict_prefers_human():
    row = CheckRow(
        "c009", "inclusion", "included", "https://x", ai_verdict="incorrect", human_verdict="correct"
    )
    assert row.final_verdict == "correct"


def test_apply_ai_verdicts_validates_entries():
    rows = check_items(sample())
    entries = [
        {"candidate_id": "c009", "item": "sectors", "ai_verdict": "incorrect", "ai_note": " fund size "},
        {"candidate_id": "c999", "item": "inclusion", "ai_verdict": "correct"},
        {"candidate_id": "c009", "item": "inclusion", "ai_verdict": "yes"},
    ]
    updated, problems = apply_ai_verdicts(rows, entries)
    by_key = {r.key: r for r in updated}
    assert by_key[("c009", "sectors")].ai_verdict == "incorrect"
    assert by_key[("c009", "sectors")].ai_note == "fund size"
    assert by_key[("c009", "inclusion")].ai_verdict == ""
    assert len(problems) == 2
