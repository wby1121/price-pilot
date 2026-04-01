# -*- coding: utf-8 -*-
"""JD — new product listings and stronger after-sales."""

from .base import Channel


class JDChannel(Channel):
    name = "jd"
    description = "京东商品搜索与比价"
    backends = ["live web search", "JD listing pages"]
    tier = 0

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "jd.com" in text or "京东" in text or "jingdong" in text

    def check(self) -> tuple[str, str]:
        return "ok", "Use live browsing for current JD pricing, reviews, and after-sales details"

