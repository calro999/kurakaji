import re, os, glob

# 1. Dictionary of polished, professional product titles (20-30 characters, clean Japanese brand + model + feature, no cuts)
refined_titles = {
    "articles/compact-coffee-maker-best7.html": [
        "パナソニック 全自動沸騰浄水 NC-A58",
        "シロカ 全自動ステンレスサーバー SC-A211",
        "シロカ コーン式全自動 カフェばこPRO CM-6C2",
        "デロンギ エレッタ 全自動コンパクトマシン",
        "シロカ 全自動ガラスサーバー SC-A211G",
        "シロカ カフェばこ タイマー付 SC-A372",
        "シロカ カフェばこ マットブラック SC-A352"
    ],
    "articles/compact-air-fryer-best7.html": [
        "Toffy ノンフライオーブントースター 2.8L",
        "Toffy ミニエアフライヤー 2.0Lスリム",
        "ハイガー 小型ノンフライヤー 2L可視化",
        "レコルト エアーオーブン ガラス窓付 2L",
        "コイズミ ノンフライクッカー レシピ付",
        "シロカ ノンフライオーブン 卓上コンパクト",
        "アイリスオーヤマ ノンフライ熱風オーブン"
    ],
    "articles/compact-electric-snow-blower-best7.html": [
        "ハイガー 40Vコードレス充電式除雪機 1200W",
        "ハイガー 100V家庭用コンセント式電動除雪機",
        "充電式コードレス手押し除雪機 LEDライト付",
        "家庭用電動除雪スコップ 20m防水コード付",
        "家庭用電動ショベル 20Vバッテリー駆動",
        "ワイド40cm手押し式電動除雪機 1200W",
        "小型軽量電動スノーブロワ 住宅街静音仕様"
    ],
    "articles/compact-desk-cooler-fan-best7.html": [
        "氷冷対応 超音波ミスト卓上冷風機 4WAY",
        "左右首振り機能付 卓上パーソナル冷風扇",
        "4000mAh大容量充電式 コードレス冷風扇",
        "強力超音波式 900ml大容量タンク冷風扇",
        "静音DCモーター搭載 卓上コンパクト冷風機",
        "瞬間冷却ペルチェ式 ハイブリッド冷風扇",
        "USB給電式 スリムタワー型卓上パーソナルクーラー"
    ],
    "articles/compact-electric-pressure-cooker-best7.html": [
        "タイガー魔法瓶 電気圧力調理鍋 4.0L COK-B400",
        "タイガー魔法瓶 電気圧力調理鍋 2.2L COK-B220",
        "東芝 1.8気圧高圧力調理鍋 3.0L RCP-30R",
        "アイリスオーヤマ 電気圧力鍋 4.0L PC-MB4",
        "アイリスオーヤマ 2WAYグリル鍋 3.0L PC-MB3",
        "シロカ おうちシェフPRO 電気圧力鍋 2.5L",
        "アイリスオーヤマ 大容量電気圧力鍋 4.0L PC-MA4"
    ],
    "articles/compact-window-radiator-best7.html": [
        "森永エンジニアリング 窓下ヒーター 90〜120cm伸縮",
        "ウインドーラジエーター 窓下専用ヒーター 90〜120cm",
        "森永エンジニアリング 国産ラジエーター 120〜190cm",
        "新型ウインドーラジエーター 高剛性 120〜190cm",
        "ロングタイプ窓下ヒーター 結露防止 120〜190cm",
        "自然対流式 窓際結露防止ラジエーター 120cm",
        "スリム自立スタンド付 窓下専用ヒーター 90cm"
    ],
    "articles/futon-vacuum-cleaner-best7.html": [
        "アイリスオーヤマ 超吸引ふとんクリーナー 温風ダニちり",
        "深紫外線UV-C除菌ランプ搭載 布団掃除機 12000Pa",
        "コードレス充電式 軽量ふとんクリーナー 10000Pa",
        "ソウイ(SOUYI) 温風UVふとんクリーナー SY-062",
        "HEPAフィルター搭載 サイクロン式布団クリーナー",
        "高速アクティブ回転ブラシ搭載 ダニ・毛取りクリーナー",
        "軽量低重心設計 エントリー布団クリーナー UV除菌"
    ]
}

# 2. Universal, high-converting, clean "あわせて読みたい厳選ガイド" component (using zero-dependency CSS grid and 100% live working links)
related_guides_html = """
    <div style="margin-top: 50px; padding: 28px 24px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
      <h3 style="font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 18px; display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 4px; height: 18px; background: #0284c7; border-radius: 2px;"></span>
        あわせて読みたい厳選ガイド（おすすめ4選）
      </h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px;">
        <a href="/articles/compact-futon-dryer-best10.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
          <span style="color: #0284c7; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">🔥 冬の快眠・ダニ退治</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">冷たい布団を一瞬でホカホカに！小型布団乾燥機TOP10</span>
        </a>
        <a href="/articles/circulator-clothes-drying-best7.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
          <span style="color: #16a34a; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">🌀 部屋干し・節電</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">部屋干し臭ゼロ！サーキュレーターおすすめTOP7</span>
        </a>
        <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
          <span style="color: #d97706; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">💡 節電マニュアル</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">冬の電気代を月1万円削る小型家電フル活用術</span>
        </a>
        <a href="/articles/cluster/single-life-appliances-regret-top5.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease; box-shadow: 0 1px 3px rgba(0,0,0,0.02);">
          <span style="color: #dc2626; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">⚠️ 後悔防止</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">一人暮らしで買って後悔した家電ワースト5</span>
        </a>
      </div>
    </div>
"""

# Process the 7 articles for titles
for filepath, titles in refined_titles.items():
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        c = f.read()
        
    for idx, new_title in enumerate(titles, 1):
        # Replace in card h2: <h2 class="rank-item-title">第{idx}位：.*?</h2>
        h2_pat = rf'<h2 class="rank-item-title">第{idx}位：.*?</h2>'
        h2_rep = f'<h2 class="rank-item-title">第{idx}位：{new_title}</h2>'
        c = re.sub(h2_pat, h2_rep, c)
        
        # Replace in table strong: <td style="font-weight:800;">第{idx}位</td>\s*<td><strong>.*?</strong></td>
        tab_pat = rf'(<td style="font-weight:800;">第{idx}位</td>\s*<td><strong>).*?(</strong></td>)'
        tab_rep = rf'\g<1>{new_title}\g<2>'
        c = re.sub(tab_pat, tab_rep, c)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Refined product titles in {filepath}")

# Now replace broken "あわせて読みたい" across ALL HTML articles in the entire site
all_articles = glob.glob("articles/**/*.html", recursive=True) + glob.glob("articles/*.html")
replaced_related_count = 0

for a in all_articles:
    with open(a, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Check if this article has the related guides block
    if "あわせて読みたい" in content:
        # Match from <div style="margin-top: 50px... or similar heading to the end of the related block
        # Pattern covers <div style="margin-top: 50px.*?あわせて読みたい.*?</div>\s*</div>\s*</div>
        # or <div class="related-guides-2x2">...
        new_content = re.sub(
            r'<div style=\"margin-top: 50px;\">\s*<h3[^>]*>あわせて読みたい.*?</div>\s*</div>\s*</div>',
            related_guides_html.strip(),
            content,
            flags=re.DOTALL
        )
        if new_content == content:
            # Try alternate pattern
            new_content = re.sub(
                r'<h3[^>]*>あわせて読みたい.*?<div class=\"related-guides-2x2\">.*?</div>\s*</div>',
                related_guides_html.strip(),
                content,
                flags=re.DOTALL
            )
        if new_content != content:
            with open(a, "w", encoding="utf-8") as f:
                f.write(new_content)
            replaced_related_count += 1

print(f"Standardized clean, robust 'あわせて読みたい' block across {replaced_related_count} articles!")
