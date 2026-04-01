# -*- coding: utf-8 -*-
"""Xianyu — peer-to-peer used goods with higher fraud risk."""

from .base import Channel


class XianyuChannel(Channel):
    name = "xianyu"
    description = "闲鱼二手商品搜索与风险评估"
    backends = ["live web search", "Xianyu listing pages"]
    tier = 0

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "xianyu" in text or "2.taobao.com" in text or "闲鱼" in text

    def check(self) -> tuple[str, str]:
        return "ok", "Use live browsing for seller history, defect disclosure, and inspection signals"

