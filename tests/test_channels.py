# -*- coding: utf-8 -*-

from price_pilot.channels import get_all_channels, get_channel


def test_registered_channels():
    names = [channel.name for channel in get_all_channels()]
    assert names == ["jd", "taobao", "pinduoduo", "xianyu", "zhuanzhuan"]


def test_lookup_channel():
    assert get_channel("jd") is not None
    assert get_channel("missing") is None

