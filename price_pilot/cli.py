# -*- coding: utf-8 -*-
"""CLI entrypoint for Price Pilot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import Config
from .core import default_skills_dir, install_skill, skill_root, uninstall_skill
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

    install_parser = subparsers.add_parser("install", help="Install bundled skill into a skills directory.")
    install_parser.add_argument("--dir", help="Target skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.")
    install_parser.add_argument("--force", action="store_true", help="Replace an existing installation.")

    update_parser = subparsers.add_parser("update", help="Update bundled skill in a skills directory.")
    update_parser.add_argument("--dir", help="Target skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.")

    uninstall_parser = subparsers.add_parser("uninstall", help="Remove installed bundled skill.")
    uninstall_parser.add_argument("--dir", help="Target skills directory. Defaults to $CODEX_HOME/skills or ~/.codex/skills.")

    config_parser = subparsers.add_parser("config", help="Manage local Price Pilot configuration.")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    config_subparsers.add_parser("show", help="Show current configuration.")
    cookie_parser = config_subparsers.add_parser("cookie", help="Register cookie export file for a platform.")
    cookie_parser.add_argument("platform", choices=["jd", "taobao", "pinduoduo", "xianyu", "zhuanzhuan"])
    cookie_parser.add_argument("--file", required=True, help="Path to exported cookie JSON file.")

    score_parser = subparsers.add_parser("score", help="Rank normalized candidate items.")
    score_parser.add_argument("--input", required=True, help="JSON array or object with items.")

    args = parser.parse_args()

    if args.command == "doctor":
        print(format_doctor_report())
        return

    if args.command == "skill-path":
        print(skill_root())
        return

    if args.command == "install":
        skills_dir = Path(args.dir).expanduser() if args.dir else default_skills_dir()
        destination = install_skill(skills_dir, force=args.force)
        print(f"Installed skill to {destination}")
        return

    if args.command == "update":
        skills_dir = Path(args.dir).expanduser() if args.dir else default_skills_dir()
        destination = install_skill(skills_dir, force=True)
        print(f"Updated skill at {destination}")
        return

    if args.command == "uninstall":
        skills_dir = Path(args.dir).expanduser() if args.dir else default_skills_dir()
        destination = uninstall_skill(skills_dir)
        print(f"Removed skill from {destination}")
        return

    if args.command == "config":
        config = Config()
        if args.config_command == "show":
            print(json.dumps(config.to_dict(), ensure_ascii=False, indent=2))
            return
        if args.config_command == "cookie":
            config.set_cookie_file(args.platform, args.file)
            print(f"Registered cookie file for {args.platform}: {Path(args.file).expanduser()}")
            return
        config_parser.print_help()
        return

    if args.command == "score":
        items = _load_items(Path(args.input))
        print(json.dumps({"ranked_items": rank_items(items)}, ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
