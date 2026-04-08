# -*- coding: utf-8 -*-

import json
import sys
from pathlib import Path

from price_pilot.cli import main


def test_workflow_command_runs_end_to_end(tmp_path: Path, capsys):
    payload = {
        "candidates": [
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
        ],
        "replies": [
            {
                "platform": "xianyu",
                "candidate_url": "https://example.com/xianyu-switch",
                "seller_name": "闲鱼卖家A",
                "reply_text": "最低1680包邮",
            }
        ],
    }
    input_path = tmp_path / "workflow.json"
    input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    old_argv = sys.argv
    sys.argv = ["price-pilot", "workflow", "--input", str(input_path), "--inquiry-limit", "1"]
    try:
        main()
    finally:
        sys.argv = old_argv

    output = json.loads(capsys.readouterr().out)
    assert len(output["discovered_candidates"]) == 2
    assert len(output["ranked_candidates"]) == 2
    assert len(output["inquiry_queue"]) == 1
    assert output["quoted_replies"][0]["quoted_price"] == 1680.0
    assert output["decision"]["best_candidate"] is not None
    assert "推荐" in output["decision"]["decision_reason"]
