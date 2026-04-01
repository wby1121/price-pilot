# -*- coding: utf-8 -*-
"""Cookie import, validation, and status helpers."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PLATFORM_RULES = {
    "jd": {
        "domains": ["jd.com", "jingdong.com"],
        "required_names": ["pt_key", "pt_pin"],
    },
    "taobao": {
        "domains": ["taobao.com", "tmall.com"],
        "required_names": ["cookie2", "_tb_token_", "unb"],
    },
    "pinduoduo": {
        "domains": ["pinduoduo.com", "yangkeduo.com"],
        "required_names": ["api_uid", "_nano_fp"],
    },
    "xianyu": {
        "domains": ["2.taobao.com", "taobao.com", "idlefish.com"],
        "required_names": ["cookie2", "_tb_token_", "unb"],
    },
    "zhuanzhuan": {
        "domains": ["zhuanzhuan.com"],
        "required_names": ["zzptt", "uid"],
    },
}


@dataclass
class CookieCheckResult:
    ok: bool
    platform: str
    file: Path
    cookie_count: int
    matched_domains: list[str]
    present_names: list[str]
    missing_names: list[str]
    format_name: str
    message: str


def cookie_store_dir(config_dir: Path) -> Path:
    return config_dir / "cookies"


def import_cookie_file(platform: str, source: Path, target_dir: Path) -> Path:
    destination_dir = cookie_store_dir(target_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination = destination_dir / f"{platform}.json"
    shutil.copy2(source, destination)
    return destination


def _normalize_cookie_entry(entry: dict[str, Any]) -> dict[str, str] | None:
    name = entry.get("name")
    value = entry.get("value")
    domain = entry.get("domain") or entry.get("host")
    if not name or value is None:
        return None
    return {
        "name": str(name),
        "value": str(value),
        "domain": str(domain or ""),
    }


def load_cookie_file(path: Path) -> tuple[list[dict[str, str]], str]:
    payload = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(payload, list):
        cookies = [_normalize_cookie_entry(entry) for entry in payload if isinstance(entry, dict)]
        return [entry for entry in cookies if entry], "list"

    if isinstance(payload, dict):
        if isinstance(payload.get("cookies"), list):
            cookies = [_normalize_cookie_entry(entry) for entry in payload["cookies"] if isinstance(entry, dict)]
            return [entry for entry in cookies if entry], "cookies-object"
        if isinstance(payload.get("data"), list):
            cookies = [_normalize_cookie_entry(entry) for entry in payload["data"] if isinstance(entry, dict)]
            return [entry for entry in cookies if entry], "data-object"
        if all(isinstance(value, str) for value in payload.values()):
            cookies = [
                {
                    "name": key,
                    "value": value,
                    "domain": "",
                }
                for key, value in payload.items()
            ]
            return cookies, "name-value-object"

    raise ValueError("Unsupported cookie format. Expected a cookie list or object with cookies/data.")


def validate_cookie_file(platform: str, path: Path) -> CookieCheckResult:
    rules = PLATFORM_RULES[platform]
    cookies, format_name = load_cookie_file(path)
    domains = rules["domains"]
    required_names = rules["required_names"]

    matched_domains = sorted(
        {
            cookie["domain"]
            for cookie in cookies
            if any(domain in cookie["domain"] for domain in domains)
        }
    )
    present_names = sorted({cookie["name"] for cookie in cookies if cookie["name"] in required_names})
    missing_names = [name for name in required_names if name not in present_names]

    ok = bool(cookies) and bool(matched_domains or format_name == "name-value-object") and not missing_names
    if ok:
        message = f"Cookie file looks usable for {platform}"
    elif not cookies:
        message = "Cookie file contains no usable cookie entries"
    elif missing_names:
        message = f"Missing expected cookies: {', '.join(missing_names)}"
    else:
        message = f"No matching domains found for {platform}"

    return CookieCheckResult(
        ok=ok,
        platform=platform,
        file=path,
        cookie_count=len(cookies),
        matched_domains=matched_domains,
        present_names=present_names,
        missing_names=missing_names,
        format_name=format_name,
        message=message,
    )


def cookie_status(platform: str, path: Path | None) -> dict[str, Any]:
    if not path:
        return {
            "platform": platform,
            "configured": False,
            "ok": False,
            "message": "No cookie file configured",
        }
    file_path = Path(path).expanduser()
    if not file_path.exists():
        return {
            "platform": platform,
            "configured": True,
            "ok": False,
            "message": f"Configured file does not exist: {file_path}",
        }
    result = validate_cookie_file(platform, file_path)
    return {
        "platform": platform,
        "configured": True,
        "ok": result.ok,
        "file": str(file_path),
        "cookie_count": result.cookie_count,
        "matched_domains": result.matched_domains,
        "present_names": result.present_names,
        "missing_names": result.missing_names,
        "format": result.format_name,
        "message": result.message,
    }
