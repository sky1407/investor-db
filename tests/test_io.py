import json

from investordb.cli import main
from investordb.io import load_candidates, load_research
from tests.test_models import base_record


def write(path, payload):
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_load_research_separates_valid_and_invalid(tmp_path):
    write(tmp_path / "c009.json", base_record())
    write(tmp_path / "c010.json", base_record(candidate_id="c010", country="Slovakia"))
    records, errors = load_research(tmp_path)
    assert [r.candidate_id for r in records] == ["c009"]
    assert [e.path.name for e in errors] == ["c010.json"]


def test_file_name_must_match_candidate_id(tmp_path):
    write(tmp_path / "c001.json", base_record())
    records, errors = load_research(tmp_path)
    assert records == []
    assert "does not match file name" in errors[0].message


def test_malformed_json_is_reported(tmp_path):
    (tmp_path / "c009.json").write_text("{not json", encoding="utf-8")
    _, errors = load_research(tmp_path)
    assert len(errors) == 1


def test_check_schema_exit_codes(tmp_path, capsys):
    good = tmp_path / "c009.json"
    write(good, base_record())
    assert main(["check-schema", str(good)]) == 0
    bad = tmp_path / "c010.json"
    write(bad, base_record(candidate_id="c010", investor_type=None))
    assert main(["check-schema", str(good), str(bad)]) == 1
    assert "FAIL" in capsys.readouterr().out


def test_candidates_file_has_unique_ids():
    ids = [c.candidate_id for c in load_candidates()]
    assert len(ids) == len(set(ids)) > 0
