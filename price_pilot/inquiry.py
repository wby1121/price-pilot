# -*- coding: utf-8 -*-
"""Inquiry assistant: draft messages, queue confirmations, and summarize replies."""

from __future__ import annotations

import re
from dataclasses import asdict

from .models import InquiryMessage, InquiryReply, ProductCandidate


DEFAULT_QUESTIONS = [
    "请问现在最低到手价是多少？",
    "是否包邮，是否支持验货或退换？",
    "商品具体成色/版本/配件是否齐全？",
]


def build_inquiry_message(candidate: ProductCandidate, custom_questions: list[str] | None = None) -> InquiryMessage:
    """Generate a reusable inquiry message draft for a candidate."""

    questions = custom_questions or DEFAULT_QUESTIONS
    seller_name = candidate.seller.seller_name or "老板"
    opening = f"{seller_name}你好，我对这件商品感兴趣。"
    product_line = f"我看到的是「{candidate.title}」"
    if candidate.condition:
        product_line += f"，标注成色/状态为 {candidate.condition}"
    text = "\n".join([opening, product_line, *questions])
    return InquiryMessage(
        platform=candidate.platform,
        candidate_url=candidate.url,
        seller_name=candidate.seller.seller_name,
        text=text,
        confirmed=False,
    )


def build_inquiry_queue(candidates: list[ProductCandidate], limit: int = 3) -> list[InquiryMessage]:
    """Build a shortlist of inquiry drafts pending manual confirmation."""

    return [build_inquiry_message(candidate) for candidate in candidates[:limit]]


def confirm_inquiry(message: InquiryMessage) -> InquiryMessage:
    """Mark an inquiry draft as manually confirmed for sending."""

    message.confirmed = True
    return message


def parse_reply(platform: str, candidate_url: str | None, seller_name: str | None, reply_text: str) -> InquiryReply:
    """Parse a seller reply into a structured reply object."""

    quoted_price = extract_price(reply_text)
    return InquiryReply(
        platform=platform,
        candidate_url=candidate_url,
        seller_name=seller_name,
        reply_text=reply_text,
        quoted_price=quoted_price,
    )


def summarize_reply(reply: InquiryReply) -> dict:
    """Convert an inquiry reply into a compact serializable summary."""

    return asdict(reply)


def extract_price(text: str) -> float | None:
    """Extract a likely RMB price from free-form seller text."""

    matches = re.findall(r"(?:(?:¥|￥|rmb|RMB)\s*)?(\d{2,6}(?:\.\d{1,2})?)", text)
    if not matches:
        return None
    try:
        return float(matches[0])
    except ValueError:
        return None

