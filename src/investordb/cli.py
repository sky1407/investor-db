import argparse
import json
import sys
from datetime import UTC, date, datetime
from pathlib import Path

from pydantic import ValidationError

from investordb.build import FxRates, InvestorOut, build_record
from investordb.export import EXCLUDED_COLUMNS, INCLUDED_COLUMNS, excluded_row, included_row, write_csv
from investordb.fetch import PageFetcher
from investordb.io import DATA_DIR, RESEARCH_DIR, ROOT, VALIDATION_DIR, load_record, load_research, write_json
from investordb.metrics import check_items, load_rows, merge, metrics_payload, save_rows
from investordb.models import CheckResult
from investordb.verify import summarize, verify_records

CACHE_DIR = ROOT / ".cache" / "pages"
VERIFY_REPORT = VALIDATION_DIR / "verify_report.json"
INVESTORS_JSON = DATA_DIR / "investors.json"
MANUAL_CHECK = VALIDATION_DIR / "manual_check.csv"


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
        INVESTORS_JSON,
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


def cmd_metrics(args: argparse.Namespace) -> int:
    if not INVESTORS_JSON.exists():
        print("run `build` first", file=sys.stderr)
        return 1
    payload = json.loads(INVESTORS_JSON.read_text(encoding="utf-8"))
    built = [InvestorOut.model_validate(r) for r in payload["records"]]
    rows = merge(check_items(built), load_rows(MANUAL_CHECK))
    save_rows(MANUAL_CHECK, rows)
    metrics = metrics_payload(built, rows)
    write_json(VALIDATION_DIR / "metrics.json", metrics)
    for source in ("human", "combined"):
        m = metrics[source]
        print(f"[{source}] precision {m['inclusion_precision']}  exclusion {m['exclusion_accuracy']}")
    print(f"human checked: {metrics['human']['human_checked']}")
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    import uvicorn

    from investordb.server import create_app

    uvicorn.run(create_app(INVESTORS_JSON, MANUAL_CHECK), host="127.0.0.1", port=args.port)
    return 0


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
    metrics = sub.add_parser("metrics", help="sync the manual check sheet and compute accuracy")
    metrics.set_defaults(func=cmd_metrics)
    serve = sub.add_parser("serve", help="browse the database and do the manual check on localhost")
    serve.add_argument("--port", type=int, default=8000)
    serve.set_defaults(func=cmd_serve)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
