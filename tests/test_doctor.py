# -*- coding: utf-8 -*-

from price_pilot.doctor import run_doctor


def test_doctor_reports_skill_and_channels():
    report = run_doctor()
    names = [name for _, name, _ in report]
    assert "skill" in names
    assert "jd" in names
    assert "zhuanzhuan" in names

