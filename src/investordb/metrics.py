import csv
import threading
from collections import defaultdict
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Literal

from investordb.build import FieldOut, InvestorOut

Verdict = Literal["correct", "incorrect", ""]
VERDICTS: tuple[str, ...] = ("correct", "incorrect", "")
FIELD_ITEMS = ("investor_type", "sectors", "stages", "ticket_min_eur", "ticket_max_eur", "aum_eur")
COLUMNS = [
    "candidate_id",
    "item",
    "system_value",
    "source_url",
    "ai_verdict",
    "ai_note",
    "human_verdict",
    "human_note",
]
_write_lock = threading.Lock()


@dataclass(frozen=True)
class CheckRow:
    candidate_id: str
    item: str
    system_value: str
    source_url: str
    ai_verdict: Verdict = ""
    ai_note: str = ""
    human_verdict: Verdict = ""
    human_note: str = ""

    @property
    def key(self) -> tuple[str, str]:
        return self.candidate_id, self.item

    @property
    def final_verdict(self) -> Verdict:
        return self.human_verdict or self.ai_verdict


def _display(field: FieldOut) -> str:
    return "; ".join(field.value) if isinstance(field.value, list) else str(field.value)


def check_items(built: list[InvestorOut]) -> list[CheckRow]:
    rows: list[CheckRow] = []
    for out in built:
        decision = "included" if out.included else f"excluded:{out.exclusion_reason}"
        rows.append(CheckRow(out.candidate_id, "inclusion", decision, out.entity_kind.source_url))
        if not out.included:
            continue
        for name in FIELD_ITEMS:
            field: FieldOut | None = getattr(out, name)
            if field is not None and field.value is not None:
                rows.append(CheckRow(out.candidate_id, name, _display(field), field.source_url))
        latest = next((i for i in out.investments if i.status == "verified" and i.in_window), None)
        if latest:
            value = f"{latest.company} ({latest.deal_date.isoformat()})"
            rows.append(CheckRow(out.candidate_id, "latest_investment", value, latest.source_url))
    return rows


def merge(generated: list[CheckRow], existing: list[CheckRow]) -> list[CheckRow]:
    previous = {row.key: row for row in existing}
    merged: list[CheckRow] = []
    for row in generated:
        old = previous.get(row.key)
        if old and old.system_value == row.system_value:
            merged.append(
                replace(
                    row,
                    ai_verdict=old.ai_verdict,
                    ai_note=old.ai_note,
                    human_verdict=old.human_verdict,
                    human_note=old.human_note,
                )
            )
        else:
            merged.append(row)
    return merged


def _verdict(raw: str | None) -> Verdict:
    value = (raw or "").strip().lower()
    if value not in VERDICTS:
        raise ValueError(f"invalid verdict: {raw!r}")
    return value  # type: ignore[return-value]


def load_rows(path: Path) -> list[CheckRow]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            CheckRow(
                candidate_id=row["candidate_id"],
                item=row["item"],
                system_value=row["system_value"],
                source_url=row["source_url"],
                ai_verdict=_verdict(row.get("ai_verdict")),
                ai_note=row.get("ai_note") or "",
                human_verdict=_verdict(row.get("human_verdict")),
                human_note=row.get("human_note") or "",
            )
            for row in csv.DictReader(handle)
        ]


def save_rows(path: Path, rows: list[CheckRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _write_lock:
        tmp = path.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS)
            writer.writeheader()
            writer.writerows(asdict(row) for row in rows)
        tmp.replace(path)


@dataclass(frozen=True)
class Ratio:
    correct: int
    total: int

    @property
    def value(self) -> float | None:
        return self.correct / self.total if self.total else None


def _ratio(rows: list[CheckRow], human_only: bool) -> Ratio:
    verdicts = [r.human_verdict if human_only else r.final_verdict for r in rows]
    judged = [v for v in verdicts if v]
    return Ratio(sum(v == "correct" for v in judged), len(judged))


def compute_metrics(
    built: list[InvestorOut], rows: list[CheckRow], human_only: bool = False, home_country: str = "SK"
) -> dict:
    scope = {b.candidate_id for b in built if b.country == home_country}
    included = {b.candidate_id for b in built if b.included}
    in_scope = [r for r in rows if r.candidate_id in scope]
    inclusion = [r for r in in_scope if r.item == "inclusion"]
    by_field: dict[str, list[CheckRow]] = defaultdict(list)
    for row in in_scope:
        if row.item != "inclusion":
            by_field[row.item].append(row)
    included_scope = [b for b in built if b.candidate_id in scope and b.included]
    fill = {
        name: Ratio(
            sum(1 for b in included_scope if (f := getattr(b, name)) is not None and f.value is not None),
            len(included_scope),
        )
        for name in FIELD_ITEMS
    }
    ai_vs_human = [r for r in in_scope if r.ai_verdict and r.human_verdict]
    return {
        "verdict_source": "human" if human_only else "human_or_ai",
        "scope_country": home_country,
        "records_in_scope": len(scope),
        "included_in_scope": len(included_scope),
        "inclusion_precision": _ratio([r for r in inclusion if r.candidate_id in included], human_only),
        "exclusion_accuracy": _ratio([r for r in inclusion if r.candidate_id not in included], human_only),
        "field_accuracy": {name: _ratio(items, human_only) for name, items in sorted(by_field.items())},
        "fill_rate": fill,
        "human_checked": Ratio(sum(1 for r in in_scope if r.human_verdict), len(in_scope)),
        "ai_agrees_with_human": Ratio(
            sum(r.ai_verdict == r.human_verdict for r in ai_vs_human), len(ai_vs_human)
        ),
    }
