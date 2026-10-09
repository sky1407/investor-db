import argparse
import sys
from pathlib import Path

from pydantic import ValidationError

from investordb.io import load_record


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="investordb")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check-schema", help="validate research JSON files")
    check.add_argument("paths", nargs="+")
    check.set_defaults(func=cmd_check_schema)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
