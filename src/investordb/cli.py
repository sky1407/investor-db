import argparse
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from pydantic import ValidationError

from investordb.build import FxRates, build_record
from investordb.export import EXCLUDED_COLUMNS, INCLUDED_COLUMNS, excluded_row, included_row, write_csv
from investordb.fetch import PageFetcher
from investordb.io import DATA_DIR, RESEARCH_DIR, ROOT, VALIDATION_DIR, load_record, load_research, write_json
from investordb.models import CheckResult
from investordb.verify import summarize, verify_records

CACHE_DIR = ROOT / ".cache" / "pages"
VERIFY_REPORT = VALIDATION_DIR / "verify_report.json"


def cmd_check_schema(args: argparse.Namespace) -> int:
    failed = 0
    for raw in args.paths:
        path = Path(raw)
        try:
            load_record(path)
            print(f"OK    {path}")
        except (ValidationError, ValueError, OSError) as exc:
            failed += 1
            print(f"FAIL  {path}\n{exc}")
    return 1 if failed else 0


def cmd_verify(args: argparse.Namespace) -> int:
    records, errors = load_research(RESEARCH_DIR)
    for error in errors:
        print(f"SCHEMA FAIL {error.path.name}: {error.message.splitlines()[0]}", file=sys.stderr)
    with PageFetcher(cache_dir=None if args.no_cache else CACHE_DIR) as fetcher:
        report = verify_records(records, fetcher, workers=args.workers)
    summary = summarize(report)
    write_json(
        VERIFY_REPORT,
        {
            "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
            "summary": summary,
            "schema_errors": [{"file": e.path.name, "message": e.message} for e in errors],
            "records": {
                cid: {name: check.model_dump() for name, check in checks.items()}
                for cid, checks in report.items()
            },
        },
    )
    print(f"records: {len(records)}  schema errors: {len(errors)}  evidence: {summary}")
    return 1 if errors else 0


def load_verify_report(path: Path = VERIFY_REPORT) -> dict[str, dict[str, CheckResult]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        cid: {name: CheckResult.model_validate(check) for name, check in checks.items()}
        for cid, checks in payload["records"].items()
    }


def cmd_build(args: argparse.Namespace) -> int:
    records, errors = load_research(RESEARCH_DIR)
    if not VERIFY_REPORT.exists():
        print("run `verify` first", file=sys.stderr)
        return 1
    report = load_verify_report()
    missing = [r.candidate_id for r in records if r.candidate_id not in report]
    if missing:
        print(f"records not verified yet, run `verify`: {', '.join(missing)}", file=sys.stderr)
        return 1
    fx = FxRates.load(DATA_DIR / "fx_rates.json")
    as_of = date.fromisoformat(args.as_of)
    built = [build_record(r, report[r.candidate_id], fx, as_of) for r in records]
    write_json(
        DATA_DIR / "investors.json",
        {"as_of": as_of, "fx": fx.model_dump(), "records": [b.model_dump(mode="json") for b in built]},
    )
    included = [b for b in built if b.included]
    excluded = [b for b in built if not b.included]
    write_csv(DATA_DIR / "investors.csv", INCLUDED_COLUMNS, [included_row(b) for b in included])
    write_csv(DATA_DIR / "excluded.csv", EXCLUDED_COLUMNS, [excluded_row(b) for b in excluded])
    review = sum(b.needs_review for b in built)
    print(f"included: {len(included)}  excluded: {len(excluded)}  needs review: {review}")
    print(f"schema errors: {len(errors)}")
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="investordb")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check-schema", help="validate research JSON files")
    check.add_argument("paths", nargs="+")
    check.set_defaults(func=cmd_check_schema)
    verify = sub.add_parser("verify", help="fetch every source and check verbatim quotes")
    verify.add_argument("--workers", type=int, default=8)
    verify.add_argument("--no-cache", action="store_true")
    verify.set_defaults(func=cmd_verify)
    build = sub.add_parser("build", help="apply inclusion rules and export the database")
    build.add_argument("--as-of", default=date.today().isoformat())
    build.set_defaults(func=cmd_build)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
