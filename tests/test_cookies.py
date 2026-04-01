# -*- coding: utf-8 -*-

import json
from pathlib import Path

from price_pilot.cookies import analyze_probe_response, import_cookie_file, validate_cookie_file


def test_validate_cookie_file_with_list_format(tmp_path: Path):
    source = tmp_path / "taobao.json"
    source.write_text(json.dumps([
        {"name": "cookie2", "value": "abc", "domain": ".taobao.com"},
        {"name": "_tb_token_", "value": "def", "domain": ".taobao.com"},
        {"name": "unb", "value": "ghi", "domain": ".taobao.com"},
    ]), encoding="utf-8")

    result = validate_cookie_file("taobao", source)
    assert result.ok is True
    assert "cookie2" in result.present_names


def test_import_cookie_file_copies_into_target_dir(tmp_path: Path):
    source = tmp_path / "jd.json"
    source.write_text(json.dumps([
        {"name": "pt_key", "value": "a", "domain": ".jd.com"},
        {"name": "pt_pin", "value": "b", "domain": ".jd.com"},
    ]), encoding="utf-8")

    destination = import_cookie_file("jd", source, tmp_path / "config")
    assert destination.exists()
    assert destination.name == "jd.json"


def test_analyze_probe_response_detects_login_redirect():
    result = analyze_probe_response(
        "taobao",
        200,
        "https://login.taobao.com/member/login.jhtml",
        "请登录",
    )
    assert result.ok is False
    assert result.mode == "login_required"


def test_analyze_probe_response_detects_authenticated_state():
    result = analyze_probe_response(
        "taobao",
        200,
        "https://i.taobao.com/my_taobao.htm",
        "我的淘宝 已买到的宝贝 收货地址",
    )
    assert result.ok is True
    assert result.mode == "authenticated"
