# -*- coding: utf-8 -*-
"""Taobao — broad catalog and seller comparison."""

from .base import Channel


class TaobaoChannel(Channel):
    name = "taobao"
    description = "淘宝商品搜索与比价"
    backends = ["live web search", "Taobao listing pages"]
    tier = 0

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "taobao.com" in text or "淘宝" in text

    def check(self) -> tuple[str, str]:
        return "ok", "Use live browsing for Taobao listings, store signals, and buyer review photos"

