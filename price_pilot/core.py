# -*- coding: utf-8 -*-
"""Core helpers for bundled skill access and validation."""

from __future__ import annotations

from pathlib import Path


def package_root() -> Path:
    return Path(__file__).resolve().parent


def skill_root() -> Path:
    return package_root() / "skill"


def required_skill_files() -> list[str]:
    return [
        "SKILL.md",
        "references/platform-playbook.md",
        "references/ranking-rubric.md",
        "scripts/score_products.py",
    ]


def validate_skill() -> tuple[bool, list[str]]:
    root = skill_root()
    missing = [relative for relative in required_skill_files() if not (root / relative).exists()]
    return len(missing) == 0, missing

