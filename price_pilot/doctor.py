# -*- coding: utf-8 -*-
"""Doctor output for package and channel readiness."""

from __future__ import annotations

from .channels import get_all_channels
from .core import validate_skill


def run_doctor() -> list[tuple[str, str, str]]:
    status: list[tuple[str, str, str]] = []
    ok, missing = validate_skill()
    if ok:
        status.append(("ok", "skill", "Bundled skill files are present"))
    else:
        status.append(("error", "skill", f"Missing skill files: {', '.join(missing)}"))
    for channel in get_all_channels():
        channel_status, message = channel.check()
        status.append((channel_status, channel.name, message))
    return status


def format_doctor_report() -> str:
    lines = ["Price Pilot doctor", ""]
    for status, name, message in run_doctor():
        badge = {
            "ok": "[ok]",
            "warn": "[warn]",
            "off": "[off]",
            "error": "[error]",
        }.get(status, "[info]")
        lines.append(f"{badge} {name}: {message}")
    return "\n".join(lines)

