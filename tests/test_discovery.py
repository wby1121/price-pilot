# -*- coding: utf-8 -*-

from price_pilot.discovery import extract_listing_fields, normalize_manual_candidate


def test_xianyu_direct_link_normalization_prefers_item_title():
    candidate = normalize_manual_candidate({
        "url": "https://www.goofish.com/item?id=123456",
        "ocr_text": "闲鱼 Switch OLED 95新\n价格 1688元\n地区：上海",
    })
    assert candidate.platform == "xianyu"
    assert candidate.raw["listing_id"] == "123456"
    assert candidate.title == "闲鱼 Switch OLED 95新"


def test_pinduoduo_extract_listing_fields_prefers_goods_name():
    html = """
    <html><head><title>拼多多商城</title></head><body>
    <script>
    window.rawData = {"goods_name":"Switch OLED 国行现货","min_group_price":168800,"goods_id":"998877"};
    </script>
    </body></html>
    """
    fields = extract_listing_fields(
        html,
        platform="pinduoduo",
        final_url="https://mobile.yangkeduo.com/goods.html?goods_id=998877",
    )
    assert fields["title"] == "Switch OLED 国行现货"
    assert fields["price"] == 1688.0
    assert fields["listing_id"] == "998877"
