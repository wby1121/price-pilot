#!/usr/bin/env python3
"""Minimal repository-local validator for skill frontmatter and expected files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
]


def fail(message: str) -> None:
    print(f"[ERROR] {message}")
    raise SystemExit(1)


def validate_frontmatter(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter.")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail("SKILL.md frontmatter is incomplete.")
    frontmatter = parts[1]
    if "name:" not in frontmatter:
        fail("SKILL.md frontmatter must include name.")
    if "description:" not in frontmatter:
        fail("SKILL.md frontmatter must include description.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a skill folder.")
    parser.add_argument("skill_path", help="Path to the skill folder.")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        fail(f"Skill path does not exist: {skill_path}")

    for relative in REQUIRED_FILES:
        target = skill_path / relative
        if not target.exists():
            fail(f"Missing required file: {relative}")

    validate_frontmatter(skill_path / "SKILL.md")
    print("[OK] Skill structure looks valid.")


if __name__ == "__main__":
    main()

