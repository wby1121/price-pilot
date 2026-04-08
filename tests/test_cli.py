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
    assert len(output["top_recommendations"]) == 2
    assert output["top_recommendations"][0]["url"] == "https://example.com/xianyu-switch"
    assert len(output["inquiry_queue"]) == 1
    assert output["quoted_replies"][0]["quoted_price"] == 1680.0
    assert output["decision"]["best_candidate"] is not None
    assert len(output["decision"]["top_recommendations"]) == 2
    assert "推荐" in output["decision"]["decision_reason"]


def test_discover_command_normalizes_manual_inputs(tmp_path: Path, capsys):
    payload = {
        "query": "Switch OLED 二手",
        "platforms": ["jd", "taobao", "xianyu", "zhuanzhuan"],
        "manual_inputs": [
            {
                "url": "https://www.goofish.com/item?id=123",
                "ocr_text": "闲鱼 Switch OLED 95新\n价格 1688元\n地区：上海\n发布时间：2026-04-08 10:00",
                "seller_name": "闲鱼卖家A",
                "screenshot_path": "/tmp/switch.png",
            }
        ],
    }
    input_path = tmp_path / "discover.json"
    input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    old_argv = sys.argv
    sys.argv = ["price-pilot", "discover", "--input", str(input_path)]
    try:
        main()
    finally:
        sys.argv = old_argv

    output = json.loads(capsys.readouterr().out)
    assert output["query"] == "Switch OLED 二手"
    assert output["normalized_candidates"][0]["platform"] == "xianyu"
    assert output["normalized_candidates"][0]["title"] == "闲鱼 Switch OLED 95新"
    assert output["normalized_candidates"][0]["price"] == 1688.0
    assert output["normalized_candidates"][0]["source_type"] == "screenshot"
    assert [item["platform"] for item in output["search_targets"]] == ["jd", "taobao"]
    source_status = {item["platform"]: item for item in output["source_status"]}
    assert source_status["xianyu"]["search_mode"] == "js_shell"
    assert source_status["zhuanzhuan"]["search_mode"] == "manual_link_only"


def test_inquiry_send_command_records_trace(tmp_path: Path, capsys):
    payload = {
        "inquiry_queue": [
            {
                "platform": "xianyu",
                "candidate_url": "https://example.com/xianyu-switch",
                "seller_name": "闲鱼卖家A",
                "text": "你好，请问最低多少钱？",
                "confirmed": False,
            }
        ]
    }
    input_path = tmp_path / "inquiry.json"
    log_dir = tmp_path / "logs"
    input_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    old_argv = sys.argv
    sys.argv = [
        "price-pilot",
        "inquiry",
        "send",
        "--input",
        str(input_path),
        "--confirm",
        "--log-dir",
        str(log_dir),
    ]
    try:
        main()
    finally:
        sys.argv = old_argv

    output = json.loads(capsys.readouterr().out)
    assert output["results"][0]["ok"] is True
    trace_files = list(log_dir.glob("*.jsonl"))
    assert trace_files
    assert "Inquiry recorded" in output["results"][0]["message"]
