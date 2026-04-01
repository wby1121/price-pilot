# -*- coding: utf-8 -*-
"""CLI entrypoint for Price Pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import skill_root
from .doctor import format_doctor_report
from .ranking import rank_items


def _load_items(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    raise ValueError("Input must be a JSON array or an object with an 'items' array.")


def main() -> None:
    parser = argparse.ArgumentParser(prog="price-pilot")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("doctor", help="Show package and platform readiness.")
    subparsers.add_parser("skill-path", help="Print bundled skill path.")

    score_parser = subparsers.add_parser("score", help="Rank normalized candidate items.")
    score_parser.add_argument("--input", required=True, help="JSON array or object with items.")

    args = parser.parse_args()

    if args.command == "doctor":
        print(format_doctor_report())
        return

    if args.command == "skill-path":
        print(skill_root())
        return

    if args.command == "score":
        items = _load_items(Path(args.input))
        print(json.dumps({"ranked_items": rank_items(items)}, ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()

