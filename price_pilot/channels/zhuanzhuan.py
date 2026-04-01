# -*- coding: utf-8 -*-
"""Zhuanzhuan — used goods with stronger inspection options."""

from .base import Channel


class ZhuanzhuanChannel(Channel):
    name = "zhuanzhuan"
    description = "转转二手商品搜索与风险评估"
    backends = ["live web search", "Zhuanzhuan listing pages"]
    tier = 0

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "zhuanzhuan" in text or "转转" in text

    def check(self) -> tuple[str, str]:
        return "ok", "Use live browsing for inspection-backed used listings and return-window details"

