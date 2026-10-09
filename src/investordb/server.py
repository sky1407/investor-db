import json
import threading
from dataclasses import asdict, replace
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from investordb.build import InvestorOut
from investordb.metrics import CheckRow, Verdict, check_items, load_rows, merge, metrics_payload, save_rows

WEB_DIR = Path(__file__).resolve().parent / "web"


class VerdictIn(BaseModel):
    human_verdict: Verdict
    human_note: str = Field(default="", max_length=500)


def create_app(data_path: Path, check_path: Path) -> FastAPI:
    app = FastAPI(title="investordb", docs_url=None, redoc_url=None)
    lock = threading.Lock()

    def load_built() -> tuple[dict, list[InvestorOut]]:
        try:
            payload = json.loads(data_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise HTTPException(503, "data/investors.json missing, run `build` first") from exc
        return payload, [InvestorOut.model_validate(r) for r in payload["records"]]

    def current_rows(built: list[InvestorOut]) -> list[CheckRow]:
        return merge(check_items(built), load_rows(check_path))

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @app.get("/api/investors")
    def investors() -> dict:
        payload, _ = load_built()
        return payload

    @app.get("/api/check")
    def check_rows() -> list[dict]:
        _, built = load_built()
        with lock:
            return [asdict(row) for row in current_rows(built)]

    @app.put("/api/check/{candidate_id}/{item}")
    def set_verdict(candidate_id: str, item: str, body: VerdictIn) -> dict:
        _, built = load_built()
        with lock:
            rows = current_rows(built)
            index = next((i for i, r in enumerate(rows) if r.key == (candidate_id, item)), None)
            if index is None:
                raise HTTPException(404, "unknown check item")
            rows[index] = replace(
                rows[index], human_verdict=body.human_verdict, human_note=body.human_note.strip()
            )
            save_rows(check_path, rows)
            return asdict(rows[index])

    @app.get("/api/metrics")
    def metrics() -> dict:
        _, built = load_built()
        with lock:
            rows = current_rows(built)
        return metrics_payload(built, rows)

    return app
