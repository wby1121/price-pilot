# -*- coding: utf-8 -*-

from pathlib import Path

from price_pilot.config import Config


def test_set_cookie_file(tmp_path: Path):
    config = Config(tmp_path / "config.yaml")
    config.set_cookie_file("taobao", "/tmp/taobao.json")
    assert config.get_cookie_file("taobao") == "/tmp/taobao.json"
    assert "taobao_cookie_file" in config.to_dict()
