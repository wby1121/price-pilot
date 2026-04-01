# -*- coding: utf-8 -*-

from pathlib import Path

from price_pilot.core import install_skill, uninstall_skill


def test_install_and_uninstall_skill(tmp_path: Path):
    destination = install_skill(tmp_path)
    assert (destination / "SKILL.md").exists()
    assert (destination / "agents" / "openai.yaml").exists()
    uninstall_skill(tmp_path)
    assert not destination.exists()
