# -*- coding: utf-8 -*-
"""Pinduoduo — subsidy pricing and low-price benchmarking."""

from .base import Channel


class PinduoduoChannel(Channel):
    name = "pinduoduo"
    description = "拼多多商品搜索与比价"
    backends = ["live web search", "Pinduoduo listing pages"]
    tier = 0

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "pinduoduo" in text or "pdd" in text or "拼多多" in text

    def check(self) -> tuple[str, str]:
        return "ok", "Use live browsing for subsidy pricing, coupon visibility, and complaint patterns"

