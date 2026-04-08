# -*- coding: utf-8 -*-
"""Product discovery helpers."""

from __future__ import annotations

from typing import Any

from .models import ProductCandidate, SellerProfile


def normalize_candidate(payload: dict[str, Any]) -> ProductCandidate:
    """Normalize a raw candidate payload into the shared ProductCandidate model."""

    seller = SellerProfile(
        seller_id=str(payload.get("seller_id")) if payload.get("seller_id") is not None else None,
        seller_name=payload.get("seller_name") or payload.get("shop_name"),
        seller_type=payload.get("seller_type"),
        reputation_score=_maybe_float(payload.get("reputation_score")),
        reputation_label=payload.get("reputation_label"),
        location=payload.get("location") or payload.get("region"),
    )

    return ProductCandidate(
        platform=str(payload.get("platform", "")),
        title=str(payload.get("title", "")),
        url=payload.get("url"),
        price=_maybe_float(payload.get("price")),
        landed_price=_maybe_float(payload.get("landed_price")),
        condition=payload.get("condition"),
        region=payload.get("region") or payload.get("location"),
        published_at=payload.get("published_at") or payload.get("created_at"),
        seller=seller,
        review_count=_maybe_int(payload.get("review_count")),
        rating=_maybe_float(payload.get("rating")),
        risk_flags=list(payload.get("risk_flags", []) or []),
        notes=list(payload.get("notes", []) or []),
        raw=dict(payload),
    )


def normalize_candidates(payloads: list[dict[str, Any]]) -> list[ProductCandidate]:
    """Normalize a list of discovery payloads."""

    return [normalize_candidate(payload) for payload in payloads]


def candidate_summary(candidate: ProductCandidate) -> dict[str, Any]:
    """Return a compact discovery summary used by scoring and decision layers."""

    return {
        "platform": candidate.platform,
        "title": candidate.title,
        "url": candidate.url,
        "price": candidate.price,
        "landed_price": candidate.landed_price,
        "condition": candidate.condition,
        "region": candidate.region,
        "seller_name": candidate.seller.seller_name,
        "seller_type": candidate.seller.seller_type,
        "reputation_score": candidate.seller.reputation_score,
        "published_at": candidate.published_at,
        "review_count": candidate.review_count,
        "rating": candidate.rating,
        "risk_flags": list(candidate.risk_flags),
    }


def _maybe_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _maybe_int(value: Any) -> int | None:
    try:
        if value is None or value == "":
            return None
        return int(value)
    except (TypeError, ValueError):
        return None

