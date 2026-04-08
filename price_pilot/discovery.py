# -*- coding: utf-8 -*-
"""Product discovery helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen

from .cookies import load_cookie_file
from .models import ProductCandidate, SellerProfile


PLATFORM_URL_PATTERNS = {
    "jd": ["jd.com", "jingdong.com"],
    "taobao": ["taobao.com", "tmall.com"],
    "pinduoduo": ["pinduoduo.com", "yangkeduo.com"],
    "xianyu": ["2.taobao.com", "goofish.com", "idlefish.com"],
    "zhuanzhuan": ["zhuanzhuan.com"],
}

PLATFORM_SEARCH_URLS = {
    "jd": "https://search.jd.com/Search?keyword={query}",
    "taobao": "https://s.taobao.com/search?q={query}",
    "pinduoduo": "https://mobile.yangkeduo.com/search_result.html?search_key={query}",
    "xianyu": "https://www.goofish.com/search?q={query}",
    "zhuanzhuan": "https://www.zhuanzhuan.com/search/?keyword={query}",
}

CONDITION_PATTERNS = [
    r"((?:99|98|95|9)新)",
    r"(全新未拆封|全新|二手|99新|95新|9成新|8成新|used|new)",
]
REGION_PATTERNS = [
    r"(?:地区|所在地|发货地|位置|城市)[:：\s]*([A-Za-z\u4e00-\u9fff·\-\s]{2,20})",
]
PUBLISHED_PATTERNS = [
    r"(?:发布时间|发布于|上架时间|发布时间间)[:：\s]*([0-9]{4}[-/.][0-9]{1,2}[-/.][0-9]{1,2}(?:\s+[0-9]{1,2}:[0-9]{2})?)",
    r"([0-9]{1,2}\s*(?:分钟|小时|天)前)",
]
TITLE_META_PATTERNS = [
    r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+name=["\']title["\'][^>]+content=["\']([^"\']+)["\']',
    r"<title>([^<]+)</title>",
]
PRICE_PATTERNS = [
    r'(?:"price"|price)[:=]\s*"?(?P<price>\d{2,7}(?:\.\d{1,2})?)',
    r"(?:¥|￥|RMB|rmb)\s*(?P<price>\d{2,7}(?:\.\d{1,2})?)",
    r"(?P<price>\d{2,7}(?:\.\d{1,2})?)\s*元",
]


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


def normalize_manual_candidate(payload: dict[str, Any]) -> ProductCandidate:
    """Normalize links, screenshots, and hand-entered notes into a candidate."""

    raw = dict(payload)
    url = payload.get("url") or payload.get("link")
    evidence_text = "\n".join(
        str(part).strip()
        for part in [
            payload.get("ocr_text"),
            payload.get("text"),
            payload.get("notes"),
            payload.get("caption"),
        ]
        if part
    )
    platform = str(
        payload.get("platform")
        or (infer_platform_from_url(str(url)) if url else None)
        or infer_platform_from_text(evidence_text)
        or "unknown"
    )

    title = (
        payload.get("title")
        or extract_title_from_text(evidence_text)
        or Path(str(payload.get("screenshot_path", ""))).stem.replace("_", " ").strip()
        or str(url or "未命名候选")
    )
    price = _maybe_float(payload.get("price")) or extract_price_from_text(evidence_text)
    condition = payload.get("condition") or extract_condition_from_text(evidence_text)
    region = payload.get("region") or payload.get("location") or extract_region_from_text(evidence_text)
    published_at = payload.get("published_at") or extract_published_at_from_text(evidence_text)
    review_count = _maybe_int(payload.get("review_count"))
    rating = _maybe_float(payload.get("rating"))
    reputation_score = _maybe_float(payload.get("reputation_score"))
    seller_name = payload.get("seller_name") or payload.get("shop_name")
    seller_type = payload.get("seller_type")
    notes = list(payload.get("notes_list", []) or [])
    if payload.get("screenshot_path"):
        notes.append(f"screenshot:{payload['screenshot_path']}")
    if evidence_text:
        notes.append("manual_evidence_attached")

    candidate = ProductCandidate(
        platform=platform,
        title=str(title),
        url=url,
        price=price,
        landed_price=_maybe_float(payload.get("landed_price")),
        condition=condition,
        region=region,
        published_at=published_at,
        seller=SellerProfile(
            seller_id=str(payload.get("seller_id")) if payload.get("seller_id") is not None else None,
            seller_name=seller_name,
            seller_type=seller_type,
            reputation_score=reputation_score,
            reputation_label=payload.get("reputation_label"),
            location=region,
        ),
        review_count=review_count,
        rating=rating,
        risk_flags=list(payload.get("risk_flags", []) or []),
        notes=notes,
        raw=raw,
    )
    candidate.raw.setdefault("source_type", payload.get("source_type") or infer_source_type(payload))
    candidate.raw.setdefault("evidence_text", evidence_text)
    return candidate


def normalize_manual_candidates(payloads: list[dict[str, Any]]) -> list[ProductCandidate]:
    """Normalize user-provided URLs, screenshots, and pasted notes."""

    return [normalize_manual_candidate(payload) for payload in payloads]


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
        "source_type": candidate.raw.get("source_type"),
    }


def infer_source_type(payload: dict[str, Any]) -> str:
    if payload.get("screenshot_path"):
        return "screenshot"
    if payload.get("url") or payload.get("link"):
        return "link"
    return "manual"


def infer_platform_from_url(url: str) -> str | None:
    if not url:
        return None
    host = urlparse(url).netloc.lower()
    for platform, domains in PLATFORM_URL_PATTERNS.items():
        if any(domain in host for domain in domains):
            return platform
    return None


def infer_platform_from_text(text: str) -> str | None:
    lowered = (text or "").lower()
    if "闲鱼" in text or "xianyu" in lowered or "goofish" in lowered:
        return "xianyu"
    if "淘宝" in text or "taobao" in lowered or "tmall" in lowered:
        return "taobao"
    if "京东" in text or "jd.com" in lowered or "jingdong" in lowered:
        return "jd"
    if "拼多多" in text or "pinduoduo" in lowered or "yangkeduo" in lowered:
        return "pinduoduo"
    if "转转" in text or "zhuanzhuan" in lowered:
        return "zhuanzhuan"
    return None


def extract_title_from_text(text: str) -> str | None:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    if not lines:
        return None
    ignored_tokens = ("价格", "地区", "所在地", "发布时间", "发货地", "卖家", "商家", "店铺")
    ranked = sorted(
        (
            line for line in lines
            if len(line) >= 4
            and not extract_price_from_text(line)
            and not any(token in line for token in ignored_tokens)
        ),
        key=len,
        reverse=True,
    )
    return ranked[0] if ranked else lines[0]


def extract_price_from_text(text: str) -> float | None:
    for pattern in PRICE_PATTERNS:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            return _maybe_float(match.group("price"))
    return None


def extract_condition_from_text(text: str) -> str | None:
    for pattern in CONDITION_PATTERNS:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_region_from_text(text: str) -> str | None:
    for pattern in REGION_PATTERNS:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_published_at_from_text(text: str) -> str | None:
    for pattern in PUBLISHED_PATTERNS:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def build_search_targets(query: str, platforms: list[str] | None = None) -> list[dict[str, str]]:
    selected = platforms or list(PLATFORM_SEARCH_URLS)
    encoded = quote_plus(query.strip())
    return [
        {
            "platform": platform,
            "search_url": PLATFORM_SEARCH_URLS[platform].format(query=encoded),
        }
        for platform in selected
        if platform in PLATFORM_SEARCH_URLS
    ]


def discover_manual_candidates(
    payloads: list[dict[str, Any]],
    fetch: bool = False,
    timeout: int = 12,
    cookie_files: dict[str, str] | None = None,
) -> tuple[list[ProductCandidate], list[dict[str, Any]]]:
    """Normalize manual evidence and optionally enrich linked candidates via HTTP."""

    candidates = normalize_manual_candidates(payloads)
    logs: list[dict[str, Any]] = []
    for candidate in candidates:
        log: dict[str, Any] = {
            "platform": candidate.platform,
            "url": candidate.url,
            "source_type": candidate.raw.get("source_type"),
            "fetched": False,
        }
        if fetch and candidate.url:
            cookie_file = None
            if cookie_files and candidate.platform in cookie_files:
                cookie_file = cookie_files[candidate.platform]
            snapshot = fetch_listing_snapshot(candidate.url, candidate.platform, cookie_file, timeout=timeout)
            log.update(snapshot)
            if snapshot.get("ok"):
                candidate.title = snapshot.get("title") or candidate.title
                candidate.price = candidate.price or _maybe_float(snapshot.get("price"))
                candidate.condition = candidate.condition or snapshot.get("condition")
                candidate.region = candidate.region or snapshot.get("region")
                candidate.published_at = candidate.published_at or snapshot.get("published_at")
                if not candidate.seller.seller_name:
                    candidate.seller.seller_name = snapshot.get("seller_name")
                candidate.raw.setdefault("fetch_snapshot", snapshot)
                candidate.notes.append("fetched_listing_snapshot")
        logs.append(log)
    return candidates, logs


def fetch_listing_snapshot(
    url: str,
    platform: str | None = None,
    cookie_file: str | None = None,
    timeout: int = 12,
) -> dict[str, Any]:
    """Fetch a direct listing URL and extract lightweight metadata."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
    }
    if cookie_file:
        cookie_path = Path(cookie_file).expanduser()
        if cookie_path.exists():
            cookies, _ = load_cookie_file(cookie_path)
            headers["Cookie"] = "; ".join(f"{entry['name']}={entry['value']}" for entry in cookies)

    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            body = response.read(65536).decode("utf-8", errors="ignore")
            extracted = extract_listing_fields(body)
            extracted.update({
                "ok": True,
                "fetched": True,
                "status_code": response.getcode(),
                "final_url": response.geturl(),
                "message": "Fetched listing snapshot successfully",
            })
            return extracted
    except HTTPError as exc:
        body = exc.read(8192).decode("utf-8", errors="ignore")
        extracted = extract_listing_fields(body)
        extracted.update({
            "ok": False,
            "fetched": False,
            "status_code": exc.code,
            "final_url": exc.geturl(),
            "message": f"Fetch returned HTTP {exc.code}",
        })
        return extracted
    except URLError as exc:
        return {
            "ok": False,
            "fetched": False,
            "status_code": None,
            "final_url": url,
            "message": f"Fetch failed: {exc.reason}",
        }


def extract_listing_fields(body: str) -> dict[str, Any]:
    """Extract title/price/condition/region/published fields from HTML or text."""

    text = body or ""
    title = None
    for pattern in TITLE_META_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            title = _clean_text(match.group(1))
            break

    price = extract_price_from_text(text)
    condition = extract_condition_from_text(text)
    region = extract_region_from_text(text)
    published_at = extract_published_at_from_text(text)
    seller_name = None
    seller_match = re.search(r"(?:卖家|店铺|商家)[:：\s]*([A-Za-z0-9_\-\u4e00-\u9fff]{2,40})", text)
    if seller_match:
        seller_name = seller_match.group(1).strip()

    return {
        "title": title,
        "price": price,
        "condition": condition,
        "region": region,
        "published_at": published_at,
        "seller_name": seller_name,
    }


def _clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


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
