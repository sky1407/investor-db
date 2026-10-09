import csv
import json
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from investordb.models import ResearchRecord

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RESEARCH_DIR = ROOT / "research"
VALIDATION_DIR = ROOT / "validation"


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    name: str
    discovery_source: str
    discovery_url: str
    retrieved_at: str


@dataclass(frozen=True)
class LoadError:
    path: Path
    message: str


def load_candidates(path: Path = DATA_DIR / "candidates.csv") -> list[Candidate]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [Candidate(**row) for row in csv.DictReader(handle)]


def load_record(path: Path) -> ResearchRecord:
    record = ResearchRecord.model_validate_json(path.read_text(encoding="utf-8"))
    if record.candidate_id != path.stem:
        raise ValueError(f"candidate_id {record.candidate_id} does not match file name {path.name}")
    return record


def load_research(directory: Path = RESEARCH_DIR) -> tuple[list[ResearchRecord], list[LoadError]]:
    records: list[ResearchRecord] = []
    errors: list[LoadError] = []
    for path in sorted(directory.glob("c*.json")):
        try:
            records.append(load_record(path))
        except (ValidationError, ValueError, OSError) as exc:
            errors.append(LoadError(path, str(exc)))
    return records, errors


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    tmp.replace(path)
