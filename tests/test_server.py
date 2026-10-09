import json
import threading

import pytest
from fastapi.testclient import TestClient

from investordb.metrics import load_rows
from investordb.server import create_app
from tests.test_metrics import sample


@pytest.fixture
def paths(tmp_path):
    data = tmp_path / "investors.json"
    data.write_text(
        json.dumps({"as_of": "2026-10-09", "records": [b.model_dump(mode="json") for b in sample()]}),
        encoding="utf-8",
    )
    return data, tmp_path / "manual_check.csv"


@pytest.fixture
def client(paths):
    return TestClient(create_app(*paths))


def test_index_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Databáza investorov" in response.text


def test_investors_endpoint(client):
    records = client.get("/api/investors").json()["records"]
    assert {r["candidate_id"] for r in records} == {"c009", "c010", "c011"}


def test_put_verdict_persists_to_csv(client, paths):
    response = client.put(
        "/api/check/c009/inclusion", json={"human_verdict": "correct", "human_note": " ok "}
    )
    assert response.status_code == 200
    assert response.json()["human_note"] == "ok"
    saved = {r.key: r for r in load_rows(paths[1])}
    assert saved[("c009", "inclusion")].human_verdict == "correct"
    rows = {(r["candidate_id"], r["item"]): r for r in client.get("/api/check").json()}
    assert rows[("c009", "inclusion")]["human_verdict"] == "correct"


def test_verdict_can_be_cleared(client):
    client.put("/api/check/c009/inclusion", json={"human_verdict": "incorrect"})
    response = client.put("/api/check/c009/inclusion", json={"human_verdict": ""})
    assert response.json()["human_verdict"] == ""


@pytest.mark.parametrize(
    "body",
    [{"human_verdict": "maybe"}, {"human_verdict": "correct", "human_note": "x" * 501}, {}],
)
def test_invalid_payload_is_rejected(client, body):
    assert client.put("/api/check/c009/inclusion", json=body).status_code == 422


def test_unknown_item_is_404(client):
    assert client.put("/api/check/c999/inclusion", json={"human_verdict": "correct"}).status_code == 404


def test_metrics_reflect_human_verdicts(client):
    client.put("/api/check/c009/inclusion", json={"human_verdict": "incorrect"})
    metrics = client.get("/api/metrics").json()
    assert metrics["human"]["inclusion_precision"] == {"correct": 0, "total": 1, "value": 0.0}
    assert metrics["human"]["records_in_scope"] == 2


def test_missing_data_returns_503(tmp_path):
    client = TestClient(create_app(tmp_path / "none.json", tmp_path / "check.csv"))
    assert client.get("/api/investors").status_code == 503


def test_concurrent_writes_do_not_lose_verdicts(client, paths):
    items = [r["item"] for r in client.get("/api/check").json() if r["candidate_id"] == "c009"]

    def put(item):
        client.put(f"/api/check/c009/{item}", json={"human_verdict": "correct"})

    threads = [threading.Thread(target=put, args=(item,)) for item in items]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    saved = [r for r in load_rows(paths[1]) if r.candidate_id == "c009"]
    assert all(r.human_verdict == "correct" for r in saved)
