# -*- coding: utf-8 -*-

from price_pilot.decision import aggregate_decision
from price_pilot.discovery import normalize_candidates
from price_pilot.inquiry import build_inquiry_queue, parse_reply
from price_pilot.scoring import score_candidates


def test_module_pipeline_runs_without_inquiry_transport():
    candidates = normalize_candidates([
        {
            "platform": "xianyu",
            "title": "Switch OLED 95新",
            "price": 1688,
            "condition": "95新",
            "region": "Shanghai",
            "seller_name": "闲鱼卖家A",
            "seller_type": "personal seller",
            "reputation_score": 0.72,
            "published_at": "2026-04-08T10:00:00Z",
            "risk_flags": ["no_inspection"],
            "url": "https://example.com/xianyu-switch",
        },
        {
            "platform": "zhuanzhuan",
            "title": "Switch OLED 官方验机",
            "price": 1820,
            "condition": "used",
            "region": "Beijing",
            "seller_name": "转转卖家B",
            "seller_type": "inspection seller",
            "reputation_score": 0.91,
            "published_at": "2026-04-07T10:00:00Z",
            "url": "https://example.com/zhuanzhuan-switch",
        },
    ])

    scored = score_candidates(candidates)
    queue = build_inquiry_queue(candidates, limit=1)
    reply = parse_reply("xianyu", candidates[0].url, candidates[0].seller.seller_name, "最低1680包邮")
    report = aggregate_decision(scored, [reply])

    assert len(scored) == 2
    assert len(queue) == 1
    assert reply.quoted_price == 1680.0
    assert report.best_candidate is not None
    assert "推荐" in report.decision_reason
