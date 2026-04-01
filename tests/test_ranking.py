# -*- coding: utf-8 -*-

from price_pilot.ranking import rank_items


def test_rank_items_prefers_better_value():
    items = [
        {
            "platform": "jd",
            "title": "A",
            "price": 7299,
            "landed_price": 7099,
            "condition": "new",
            "seller_type": "official flagship",
            "rating": 4.9,
            "review_count": 3400,
            "warranty": "1 year",
            "return_policy": "7 days",
            "advantages": ["official store"],
            "red_flags": [],
            "url": "https://example.com/jd",
        },
        {
            "platform": "xianyu",
            "title": "B",
            "price": 5988,
            "landed_price": 5988,
            "condition": "used",
            "seller_type": "personal seller",
            "rating": 4.4,
            "review_count": 23,
            "advantages": ["cheap"],
            "red_flags": ["battery unknown"],
            "risk_flags": ["unknown_condition", "no_inspection"],
            "url": "https://example.com/xianyu",
        },
    ]
    ranked = rank_items(items)
    assert ranked[0]["platform"] == "xianyu"
    assert ranked[1]["platform"] == "jd"

