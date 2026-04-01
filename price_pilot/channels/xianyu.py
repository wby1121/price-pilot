# -*- coding: utf-8 -*-
"""Xianyu — peer-to-peer used goods with higher fraud risk."""

from .base import Channel
from ..integrations.mcporter import has_platform_server


class XianyuChannel(Channel):
    name = "xianyu"
    description = "闲鱼二手商品搜索与风险评估"
    backends = ["live web search", "Xianyu listing pages"]
    tier = 0

    def can_handle(self, text: str) -> bool:
        text = text.lower()
        return "xianyu" in text or "2.taobao.com" in text or "闲鱼" in text

    def check(self, config=None) -> tuple[str, str]:
        if has_platform_server("xianyu"):
            return "ok", "mcporter Xianyu server is configured"
        cookie_file = config.get_cookie_file("xianyu") if config else None
        if cookie_file:
            return "warn", f"Cookie configured at {cookie_file}; MCP server not configured yet"
        return "off", "Need Xianyu cookie export or mcporter server before stable live access"
