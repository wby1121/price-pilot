# -*- coding: utf-8 -*-
"""Helpers for reading mcporter configuration."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATHS = [
    Path.home() / ".openclaw" / "workspace" / "config" / "mcporter.json",
    Path.home() / ".config" / "mcporter" / "config.json",
]

PLATFORM_ALIASES = {
    "jd": ["jd", "jingdong"],
    "taobao": ["taobao"],
    "pinduoduo": ["pinduoduo", "pdd"],
    "xianyu": ["xianyu"],
    "zhuanzhuan": ["zhuanzhuan", "zhuan", "zz"],
}


def locate_mcporter_config() -> Path | None:
    env_path = os.environ.get("MCPORTER_CONFIG")
    if env_path:
        path = Path(env_path).expanduser()
        if path.exists():
            return path
    for path in DEFAULT_CONFIG_PATHS:
        if path.exists():
            return path
    return None


def load_mcporter_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or locate_mcporter_config()
    if not config_path:
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def list_mcporter_servers(path: Path | None = None) -> list[str]:
    data = load_mcporter_config(path)
    servers = data.get("mcpServers", {})
    if isinstance(servers, dict):
        return sorted(servers.keys())
    return []


def has_platform_server(platform: str, path: Path | None = None) -> bool:
    aliases = PLATFORM_ALIASES.get(platform, [platform])
    servers = set(list_mcporter_servers(path))
    return any(alias in servers for alias in aliases)

