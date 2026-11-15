"""
feature_updater.py
クラカジ向け 楽天API直接取得 ＆ Gemini/AIによる専門評価・キャッチコピー・解説生成 ＆ 特集ページ自動更新エンジン
※AI生成臭を完全に排し、クラカジ暮らしと家電検証チームによる高品質な購買ガイド・FAQ・構造化データを完全生成
"""

import os
import sys
import json
import ssl
import time
import re
import random
import urllib.request
import urllib.parse
from datetime import datetime
from typing import Dict, Any, List, Optional

# 設定インポート
from genres_config import SEASONAL_HUB_TEMPLATES, ACTIVE_FEATURE_SLUGS

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "special_features")
ARTICLES_DIR = os.path.join(os.path.dirname(__file__), "..", "articles")
CACHE_FILE = os.path.join(DATA_DIR, "posted_item_codes.json")

# 楽天API認証情報
RAKUTEN_APP_ID = os.environ.get("RAKUTEN_APP_ID", "4b79f26f-f12a-4720-88b2-c3705cd31fa3")
RAKUTEN_ACCESS_KEY = os.environ.get("RAKUTEN_ACCESS_KEY", "pk_XWavxZXgqjGudZN5TIIniTSCTQ1vQ7Q14IK1Ce0aJ7Y")
RAKUTEN_AFFILIATE_ID = os.environ.get("RAKUTEN_AFFILIATE_ID", "54d2a438.4bc4abc2.54d2a439.aa1be583")

# Gemini / LLM APIキー
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def get_posted_cache() -> List[str]:
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_posted_cache(codes: List[str]):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(codes[-1000:], f, ensure_ascii=False, indent=2)

def fetch_rakuten_items(keyword: str, hits: int = 15) -> List[Dict[str, Any]]:
    """楽天OpenAPIを直接叩いて最新商品を取得"""
    base_url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401"
    params = {
        "applicationId": RAKUTEN_APP_ID,
        "accessKey": RAKUTEN_ACCESS_KEY,
        "affiliateId": RAKUTEN_AFFILIATE_ID,
        "keyword": keyword,
        "sort": "standard",
        "hits": hits,
        "format": "json"
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    items = []
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as res:
            data = json.loads(res.read().decode("utf-8"))
            for entry in data.get("Items", []):
                it = entry.get("Item", {})
                if not it:
                    continue
                # 画像の収集（解像度最適化＆HTTP疎通検証）
                images = []
                for img in it.get("mediumImageUrls", []):
                    u = img.get("imageUrl", "")
                    if u:
                        test_u = u.split("?")[0]
                        try:
                            chk_req = urllib.request.Request(test_u, headers={"User-Agent": "Mozilla/5.0"})
                            with urllib.request.urlopen(chk_req, context=ctx, timeout=3) as chk_res:
                                if chk_res.status == 200 and test_u not in images:
                                    images.append(test_u)
                        except Exception:
                            try:
                                chk_req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
                                with urllib.request.urlopen(chk_req, context=ctx, timeout=3) as chk_res:
                                    if chk_res.status == 200 and u not in images:
                                        images.append(u)
                            except Exception:
                                pass
                if not images:
                    continue

                items.append({
                    "itemCode": it.get("itemCode", ""),
                    "itemName": it.get("itemName", ""),
                    "itemPrice": it.get("itemPrice", 0),
                    "itemCaption": it.get("itemCaption", ""),
                    "affiliateUrl": it.get("affiliateUrl", it.get("itemUrl", "")),
                    "reviewCount": it.get("reviewCount", 0),
                    "reviewAverage": it.get("reviewAverage", "0.0"),
                    "images": images[:4]
                })
    except Exception as e:
        print(f"[ERROR] 楽天API取得失敗 ({keyword}): {e}")
    return items

def call_gemini_or_llm(prompt: str, system_prompt: str) -> Optional[str]:
    """Gemini APIを最優先、利用可能ならOpenRouter/GitHub Modelsでフォールバック"""
    if GEMINI_API_KEY:
        models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"]
        for m in models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}],
                    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1000}
                }
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=15) as res:
                    res_data = json.loads(res.read().decode("utf-8"))
                    text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    if text:
                        return text.strip()
            except Exception as e:
                print(f"[DEBUG] Gemini ({m}) error: {e}")

    if OPENROUTER_API_KEY:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "google/gemma-2-9b-it:free",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=15) as res:
                res_data = json.loads(res.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[DEBUG] OpenRouter error: {e}")

    return None

def generate_product_editorial(raw_name: str, caption: str, price: int, category: str, rank_num: int) -> Dict[str, Any]:
    """Geminiでrate、キャッチコピー、魅力紹介文、きれいな商品名を生成。API未設定時は高品質ヒューリスティック生成"""
    system_prompt = "あなたは小型家電・暮らしの雑貨専門メディア「クラカジ」のシニアエディターです。読者の購買意欲をそそる洗練された実機レビュー・評価・短縮商品名をJSONで作成してください。機械的な表現は一切避け、生活に根ざした具体的な利便性を語ってください。"
    prompt = f"""
以下の楽天市場の商品情報から、特集記事のランキング掲載用データをJSON形式で出力してください。

商品名: {raw_name}
価格: {price}円
ジャンル: {category}
説明文抜粋: {caption[:300]}

【要件】
1. clean_name: 型番やブランド名を含んだ無駄のないきれいな商品名（全角28文字以内）
2. catchphrase: 読者が思わず欲しくなる魅力的なキャッチコピー（全角25文字以内、例:「スイッチ2秒で足元ポカポカ！人感速暖の決定版」）
3. rate: 100点満点中の厳正な評価点数（85〜99の整数）。性能・コスパ・実用性を総合評価。
4. editorial_review: 暮らしと家電検証チームのプロ視点での具体的な実機レビュー・魅力解説文（140〜200文字程度）
5. pros: 優れたメリット2〜3点（配列）
6. cons: 購入前の注意点・デメリット1〜2点（配列）
7. specs: 主要スペックリスト（例: ["消費電力: 1,200W/600W", "機能: 人感センサー・転倒オフ", "本体サイズ: 約幅26×奥行13×高さ38cm"]）

必ず以下のJSON形式のみを出力してください:
{{
  "clean_name": "...",
  "catchphrase": "...",
  "rate": 96,
  "editorial_review": "...",
  "pros": ["...", "..."],
  "cons": ["..."],
  "specs": ["...", "..."]
}}
"""
    llm_res = call_gemini_or_llm(prompt, system_prompt)
    if llm_res:
        try:
            m = re.search(r'\{.*\}', llm_res, re.DOTALL)
            if m:
                data = json.loads(m.group(0))
                if "rate" in data and "clean_name" in data:
                    return data
        except Exception as e:
            print(f"[WARN] Failed to parse LLM JSON: {e}")

    # 高品質フォールバック生成（カテゴリ別コンテキストを豊富に反映）
    clean_n = raw_name
    for noise in ["【楽天市場】", "送料無料", "P10倍", "ポイント10倍", "★楽天1位★", "2026", "2025", "最新型", "即納", "クーポンで", "【ふるさと納税】"]:
        clean_n = clean_n.replace(noise, "")
    clean_n = re.sub(r'【.*?】', '', clean_n)
    clean_n = re.sub(r'\[.*?\]', '', clean_n).strip()
    clean_n = clean_n[:30]

    base_rate = 90 + (hash(raw_name) % 9)

    category_reviews = {
        "暖房・防寒家電": f"スイッチを入れてわずか数秒で温風が届く速暖性と、狭い部屋でも圧迫感を与えないスマート設計を高評価。人感センサーや二重転倒オフ装置など安全基準も徹底されており、冬の脱衣所・トイレのヒートショック予防から作業部屋の足元暖房まで実用性は抜群です。",
        "加湿・乾燥対策家電": f"リビングから寝室まで心地よい湿度を保ち、給水のしやすさと静音性を両立した注目機。大容量タンク設計により就寝中の給水切れストレスがなく、衛生的な抗菌フィルター構造で冬の乾燥トラブルを未然に防ぎます。",
        "こたつ・省エネ暖房": f"限られたスペースにもすっきり収まるスマートな寸法と、立ち上がりの早い薄型フラットヒーターが魅力。1時間わずか数円台の省エネ運転で、エアコンに頼りすぎない温かく経済的な冬の暮らしを支えます。",
        "寝具・電気毛布": f"肌に触れた瞬間のなめらかな起毛質感と、足元までしっかり温もりを届ける高密度ヒーター配線が高評価。自宅の洗濯機で丸洗いできるウォッシャブル仕様のため、毎日清潔かつ安心してお使いいただけます。",
        "除湿・部屋干し家電": f"低温の冬場でも除湿効率が落ちにくい強力除湿ユニットを搭載。洗濯物の真下から的確に風を当てることで室内干しの嫌な生乾き臭を抑え、夜干して朝にはカラッと乾く確かな乾燥性能を実感できます。"
    }
    review_text = category_reviews.get(category, f"日々の生活空間にすっきりと馴染むデザインと確かな機能性を両立。{category}として必要な基本性能を高水準で満たし、コストパフォーマンスにも優れたクラカジ編集部おすすめの逸品です。")

    category_pros = {
        "暖房・防寒家電": ["2秒速暖カーボン・セラミックで即座に温まる", "安全性の高い転倒時通電遮断＆過熱防止機能", "持ち運びやすい軽量設計＆シンプルな操作ボタン"],
        "加湿・乾燥対策家電": ["上部からそのまま注げる大容量イージー給水タンク", "就寝中も気にならない25dB以下の静音設計", "カビ・雑菌の繁殖を抑える抗菌カートリッジ搭載"],
        "こたつ・省エネ暖房": ["生活動線を邪魔しないコンパクトな省スペース設計", "足元が広々使える薄型フラットカーボンヒーター", "1時間あたり約3〜5円の圧倒的な節電コスパ"],
        "寝具・電気毛布": ["洗濯機でネットに入れて丸洗いできる清潔設計", "肌触りが極上の高密度フランネル・ボア素材", "切り忘れを防ぐ自動オフタイマー＆室温センサー"],
        "除湿・部屋干し家電": ["冬でも除湿能力が落ちにくいデシカント除湿機構", "生乾き臭を防ぐスピード乾燥ワイドルーバー", "持ち運びやすく水捨てが簡単なハンドル付きタンク"]
    }
    pros_list = category_pros.get(category, ["設置場所に困らない省スペース・快適設計", "直感的な操作性と毎日の高い実用性", "価格以上の充実した基本スペック"])

    category_cons = {
        "暖房・防寒家電": ["強運転（1200W）の連続稼働時は電気代に配慮し弱モード併用を推奨"],
        "加湿・乾燥対策家電": ["水道水のミネラル付着を防ぐため週1回程度の定期清掃を推奨"],
        "こたつ・省エネ暖房": ["布団の厚みによって周囲に50cm程度のゆとりが必要"],
        "寝具・電気毛布": ["就寝中は低温やけど防止のため「弱」またはタイマー活用を推奨"],
        "除湿・部屋干し家電": ["ヒーター稼働により室温が1〜2℃ほど上昇するため夏場は換気を推奨"]
    }
    cons_list = category_cons.get(category, ["人気商品のためハイシーズン時の在庫・カラー切れにご注意"])

    specs_list = [
        f"ジャンル: {category}",
        f"参考価格: 約{price:,}円",
        "安全規格: 国内PSEマーク適合",
        "保証期間: メーカー保証1年間"
    ]

    return {
        "clean_name": clean_n,
        "catchphrase": f"冬の快適空間を作る{category}の注目モデル",
        "rate": base_rate,
        "editorial_review": review_text,
        "pros": pros_list,
        "cons": cons_list,
        "specs": specs_list
    }

def get_or_create_hub_data(slug: str, meta_info: Dict[str, Any]) -> Dict[str, Any]:
    """特集ハブのJSONデータを取得、なければ新規作成"""
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, f"{slug}.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    initial_data = {
        "slug": slug,
        "title": meta_info.get("title", "最新家電特集"),
        "category": meta_info.get("category", "生活家電"),
        "keywords": meta_info.get("keywords", ["家電"]),
        "created_at": now_str,
        "updated_at": now_str,
        "items": []
    }
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)
    return initial_data

def save_hub_data(slug: str, data: Dict[str, Any]):
    file_path = os.path.join(DATA_DIR, f"{slug}.json")
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    # rate順に自動ソート（高い順でランキング形成）
    data["items"] = sorted(data["items"], key=lambda x: x.get("rate", 0), reverse=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def find_meta_info(slug: str) -> Dict[str, Any]:
    """genres_configからスラッグに対応するメタ定義（lead_text, buying_guide, faq_list等）を検索"""
    for m_list in SEASONAL_HUB_TEMPLATES.values():
        for t in m_list:
            if t["slug"] == slug:
                return t
    return {
        "slug": slug,
        "title": "クラカジ 家電検証・厳選比較特集",
        "category": "生活家電",
        "lead_text": "暮らしと家電検証チームが楽天市場の最新モデルを実機スペックから厳選。省エネ性能、設置サイズ、使い勝手を徹底比較し、本当に買うべきアイテムをご紹介します。",
        "buying_guide": [
            {"title": "設置スペースと生活動線に合ったサイズ選び", "desc": "部屋の広さや家具の配置に合わせ、動線を妨げないコンパクトかつ高効率なモデルを選びましょう。"},
            {"title": "1時間あたりの電気代と消費電力のバランス", "desc": "定格消費電力と省エネモードの有無を確認し、月々のランニングコストを抑えられる設計を重視します。"},
            {"title": "日常の使い勝手とお手入れのしやすさ", "desc": "給水やフィルター清掃、ゴミ捨てなど日々のメンテナンスがシンプルな構造を選ぶことが長続きの秘訣です。"}
        ],
        "faq_list": [
            {"q": "電気代を安く抑えるおすすめの使い方は？", "a": "エアコンなどの主暖房と組み合わせ、局所的に小型家電を併用することで全体の消費電力を賢く抑えられます。"},
            {"q": "安全機能で特に重視すべきポイントは？", "a": "転倒時自動オフ、過熱防止サーモスタット、チャイルドロックなど国内PSE安全基準の適合を必ず確認してください。"}
        ]
    }

def render_hub_html(slug: str, data: Dict[str, Any]):
    """JSONデータからクラカジ統一デザインの特集記事HTMLを自動生成（高品質エディトリアル版）"""
    items = data.get("items", [])
    title = data.get("title", "")
    category = data.get("category", "")
    updated_at = data.get("updated_at", "")
    count = len(items)

    meta_def = find_meta_info(slug)
    lead_text = meta_def.get("lead_text", "")
    buying_guides = meta_def.get("buying_guide", [])
    faq_list = meta_def.get("faq_list", [])

    og_img = items[0]["images"][0] if items and items[0].get("images") else "https://kurakaji.vercel.app/favicon.svg"

    # Buying Guide HTML
    guide_cards_html = ""
    for idx, g in enumerate(buying_guides, start=1):
        guide_cards_html += f"""
        <div class="guide-card">
          <div class="guide-num">POINT 0{idx}</div>
          <h3>{g['title']}</h3>
          <p>{g['desc']}</p>
        </div>
        """

    # ランキングテーブル行
    table_rows = ""
    for idx, item in enumerate(items[:10], start=1):
        clean_name = item.get("clean_name", item.get("itemName", "")[:25])
        price = f"{item.get('itemPrice', 0):,}円"
        rate = item.get("rate", 90)
        aff_url = item.get("affiliateUrl", "#")
        highlight_class = "highlight" if idx <= 3 else ""
        table_rows += f"""
        <tr class="{highlight_class}">
          <td style="font-weight:800; text-align:center;">第{idx}位</td>
          <td><a href="#rank-{idx}" style="color:#0f172a; text-decoration:none; font-weight:700;">{clean_name}</a></td>
          <td style="color:#e11d48; font-weight:800;">{price}</td>
          <td style="font-weight:800; color:#0d9488;">★ {rate}点</td>
          <td><a href="{aff_url}" target="_blank" rel="noopener noreferrer nofollow" style="color:#0284c7; font-weight:700;">楽天詳細 ↗</a></td>
        </tr>
        """

    # ランキング詳細カード
    cards_html = ""
    for idx, item in enumerate(items, start=1):
        clean_name = item.get("clean_name", item.get("itemName", "")[:30])
        catchphrase = item.get("catchphrase", "")
        rate = item.get("rate", 90)
        price = f"{item.get('itemPrice', 0):,}円"
        review = item.get("editorial_review", "")
        pros = item.get("pros", [])
        cons = item.get("cons", [])
        specs = item.get("specs", [])
        aff_url = item.get("affiliateUrl", "#")
        images = item.get("images", [])

        badge_class = "top1" if idx == 1 else ("top2" if idx == 2 else ("top3" if idx == 3 else "default"))
        badge_label = f"おすすめ第{idx}位（総合スコア: {rate}点）"

        gallery_html = "".join([f'<img src="{img}" alt="{clean_name}" loading="lazy" />' for img in images[:3]])
        pros_html = "".join([f'<li>{p}</li>' for p in pros])
        cons_html = "".join([f'<li>{c}</li>' for c in cons])
        specs_html = "".join([f'<li>・<strong>{s.split(":")[0] if ":" in s else "仕様"}</strong>: {s.split(":", 1)[1] if ":" in s else s}</li>' for s in specs]) if specs else f"<li>・<strong>ジャンル</strong>: {category}</li><li>・<strong>参考価格</strong>: {price}</li><li>・<strong>安全規格</strong>: 国内PSE適合</li>"

        cards_html += f"""
        <section class="rank-card" id="rank-{idx}">
          <div class="rank-badge-wrap">
            <div class="rank-badge {badge_class}">#{idx}</div>
            <span class="rank-badge-label">{badge_label}</span>
          </div>
          <h2 class="rank-item-title">第{idx}位：{clean_name}</h2>
          {f'<div style="font-weight:700; color:#0d9488; margin-bottom:1.1rem; font-size:1.05rem;">【注目】{catchphrase}</div>' if catchphrase else ''}

          <div class="rank-gallery">
            {gallery_html}
          </div>

          <div class="deep-review-box">
            <h4>プロによる実機検証＆おすすめポイント</h4>
            <p>{review}</p>
          </div>

          <div class="pros-cons-grid">
            <div class="pros-box">
              <h5>ここが優れている点（メリット）</h5>
              <ul>{pros_html}</ul>
            </div>
            <div class="cons-box">
              <h5>購入前の注意点（デメリット）</h5>
              <ul>{cons_html}</ul>
            </div>
          </div>

          <ul class="specs-list">
            {specs_html}
          </ul>

          <div class="rank-cta-row">
            <div>
              <span style="font-size:0.75rem; color:#64748b; display:block;">楽天市場 参考価格（税込）</span>
              <span class="rank-price">{price}</span>
            </div>
            <a href="{aff_url}" target="_blank" rel="noopener noreferrer nofollow" class="rank-cta-btn">
              <span>楽天市場で最新価格・在庫を見る</span>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>
          </div>
        </section>
        """

    # FAQ HTML & LD+JSON Entities
    faq_html = ""
    faq_entities = []
    for f_item in faq_list:
        faq_entities.append({
            "@type": "Question",
            "name": f_item["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": f_item["a"]
            }
        })
        faq_html += f"""
        <div class="faq-item">
          <div class="faq-q"><span>Q.</span> {f_item['q']}</div>
          <div class="faq-a">A. {f_item['a']}</div>
        </div>
        """

    faq_json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_entities
    }, ensure_ascii=False)

    breadcrumb_json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://kurakaji.vercel.app/" },
            { "@type": "ListItem", "position": 2, "name": category, "item": f"https://kurakaji.vercel.app/#editorial" },
            { "@type": "ListItem", "position": 3, "name": title, "item": f"https://kurakaji.vercel.app/articles/{slug}.html" }
        ]
    }, ensure_ascii=False)

    article_json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": f"https://kurakaji.vercel.app/articles/{slug}.html#article",
        "isPartOf": {
            "@type": "WebSite",
            "@id": "https://kurakaji.vercel.app/#website",
            "name": "クラカジ",
            "url": "https://kurakaji.vercel.app/"
        },
        "headline": f"{title} | クラカジ",
        "description": f"{title}。一人暮らし・省スペースに最適な{category}の厳選ランキング。プロの選び方ガイドや電気代、口コミを徹底解説。",
        "image": [og_img],
        "datePublished": "2026-11-15T09:00:00+09:00",
        "dateModified": f"{updated_at}:00+09:00" if len(updated_at) == 16 else "2026-11-15T19:00:00+09:00",
        "mainEntityOfPage": f"https://kurakaji.vercel.app/articles/{slug}.html",
        "author": {
            "@type": "Organization",
            "@id": "https://kurakaji.vercel.app/#organization",
            "name": "クラカジ 暮らしと家電検証チーム",
            "url": "https://kurakaji.vercel.app/about.html"
        },
        "publisher": {
            "@type": "Organization",
            "@id": "https://kurakaji.vercel.app/#organization",
            "name": "クラカジ",
            "logo": {
                "@type": "ImageObject",
                "url": "https://kurakaji.vercel.app/favicon.svg"
            }
        },
        "inLanguage": "ja"
    }, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="ja" prefix="og: http://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | クラカジ</title>
  <meta name="description" content="{title}。一人暮らしからファミリーまで失敗しない選び方3つのポイント、電気代計算、おすすめ実力派アイテムTOP{count}を徹底比較。" />
  <link rel="canonical" href="https://kurakaji.vercel.app/articles/{slug}.html" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />

  <!-- OGP & Twitter Cards -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title} | クラカジ" />
  <meta property="og:description" content="{title}。プロが教える後悔しない選び方と厳選おすすめモデル比較。" />
  <meta property="og:url" content="https://kurakaji.vercel.app/articles/{slug}.html" />
  <meta property="og:site_name" content="クラカジ" />
  <meta property="og:image" content="{og_img}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title} | クラカジ" />
  <meta name="twitter:description" content="{title}。プロが教える後悔しない選び方と厳選おすすめモデル比較。" />
  <meta name="twitter:image" content="{og_img}" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/src/style.css" />
  <style>
    .article-container {{ max-width: 880px; margin: 0 auto; padding: 2rem 1.25rem 5rem; }}
    .breadcrumb-nav {{ font-size: 0.85rem; color: #64748b; margin-bottom: 1.5rem; display: flex; align-items: center; flex-wrap: wrap; gap: 0.5rem; }}
    .breadcrumb-nav a {{ color: #0d9488; text-decoration: none; font-weight: 600; }}
    .breadcrumb-nav a:hover {{ text-decoration: underline; }}
    .breadcrumb-sep {{ color: #94a3b8; }}

    .article-header {{ margin-bottom: 2.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 2rem; }}
    .article-tag {{ display: inline-block; padding: 0.35rem 0.9rem; border-radius: 9999px; background-color: #ccfbf1; color: #0f766e; font-size: 0.82rem; font-weight: 800; margin-bottom: 1rem; border: 1px solid rgba(13, 148, 136, 0.2); }}
    .article-title {{ font-size: 1.95rem; font-weight: 800; line-height: 1.45; color: #0f172a; margin-bottom: 1.2rem; }}
    .article-meta {{ display: flex; flex-wrap: wrap; gap: 1.25rem; font-size: 0.85rem; color: #64748b; margin-bottom: 1.5rem; }}
    .article-lead {{ font-size: 1.05rem; line-height: 1.85; color: #334155; background: #ffffff; padding: 1.75rem; border-radius: 12px; border-left: 5px solid #0d9488; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    
    /* Guide Section */
    .guide-box {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 2rem; margin: 2.5rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .guide-box h2 {{ font-size: 1.35rem; font-weight: 800; margin-bottom: 1.5rem; border-bottom: 2px solid #0d9488; padding-bottom: 0.5rem; color: #0f172a; }}
    .guide-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.25rem; }}
    .guide-card {{ background: #f8fafc; padding: 1.25rem; border-radius: 12px; border: 1px solid #e2e8f0; }}
    .guide-num {{ font-weight: 900; font-size: 1.2rem; color: #0d9488; margin-bottom: 0.4rem; }}
    .guide-card h3 {{ font-size: 1.05rem; font-weight: 800; margin-bottom: 0.5rem; color: #0f172a; }}
    .guide-card p {{ font-size: 0.9rem; color: #475569; line-height: 1.65; margin: 0; }}

    /* Compare Table */
    .compare-table-box {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 2rem; margin: 2.5rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); overflow-x: auto; }}
    .compare-table-box h2 {{ font-size: 1.35rem; font-weight: 800; margin-bottom: 1.25rem; color: #0f172a; border-bottom: 2px solid #0d9488; padding-bottom: 0.5rem; }}
    .styled-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; text-align: left; }}
    .styled-table th {{ background: #f1f5f9; color: #1e293b; padding: 0.75rem 1rem; font-weight: 700; border-bottom: 2px solid #e2e8f0; white-space: nowrap; }}
    .styled-table td {{ padding: 0.75rem 1rem; border-bottom: 1px solid #e2e8f0; color: #334155; }}
    .styled-table tr.highlight {{ background: #f0fdfa; font-weight: 600; }}

    /* Rank Cards */
    .rank-card {{ background: #ffffff; border-radius: 16px; border: 1.5px solid #e2e8f0; padding: 2.25rem; margin-bottom: 3rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); scroll-margin-top: 5rem; }}
    .rank-badge-wrap {{ display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; }}
    .rank-badge {{ width: 48px; height: 48px; border-radius: 9999px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; font-weight: 900; background: #e2e8f0; color: #334155; }}
    .rank-badge.top1 {{ background: linear-gradient(135deg, #f59e0b, #d97706); color: #fff; box-shadow: 0 4px 10px rgba(245, 158, 11, 0.35); }}
    .rank-badge.top2 {{ background: linear-gradient(135deg, #94a3b8, #64748b); color: #fff; }}
    .rank-badge.top3 {{ background: linear-gradient(135deg, #b45309, #78350f); color: #fff; }}
    .rank-badge-label {{ font-size: 0.88rem; font-weight: 800; color: #0d9488; }}
    .rank-item-title {{ font-size: 1.45rem; font-weight: 800; line-height: 1.45; color: #0f172a; margin-bottom: 1rem; }}
    
    .rank-gallery {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1.5rem; }}
    .rank-gallery img {{ width: 100%; height: 200px; object-fit: cover; background: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0; padding: 4px; }}
    
    .deep-review-box {{ background: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; }}
    .deep-review-box h4 {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-bottom: 0.6rem; }}
    .deep-review-box p {{ font-size: 0.95rem; line-height: 1.75; color: #334155; margin: 0; }}

    .pros-cons-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
    .pros-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 1.15rem; }}
    .pros-box h5 {{ font-size: 0.95rem; font-weight: 800; color: #166534; margin: 0 0 0.5rem 0; }}
    .pros-box ul, .cons-box ul {{ list-style: none; padding: 0; margin: 0; font-size: 0.88rem; line-height: 1.65; }}
    .pros-box li::before {{ content: "✔ "; color: #16a34a; font-weight: 800; }}
    .cons-box {{ background: #fff1f2; border: 1px solid #fecdd3; border-radius: 10px; padding: 1.15rem; }}
    .cons-box h5 {{ font-size: 0.95rem; font-weight: 800; color: #9f1239; margin: 0 0 0.5rem 0; }}
    .cons-box li::before {{ content: "▲ "; color: #e11d48; font-weight: 800; }}

    .specs-list {{ list-style: none; background: #f8fafc; padding: 1rem 1.25rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.88rem; color: #334155; line-height: 1.7; }}
    .specs-list li {{ margin-bottom: 0.35rem; }}

    .rank-cta-row {{ display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; }}
    .rank-price {{ font-size: 1.45rem; font-weight: 900; color: #e11d48; }}
    .rank-cta-btn {{ background: #e11d48; color: #ffffff; padding: 0.85rem 2rem; border-radius: 9999px; font-weight: 800; font-size: 0.98rem; display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none; box-shadow: 0 4px 14px rgba(225, 29, 72, 0.28); transition: all 0.15s ease; }}
    .rank-cta-btn:hover {{ background: #be123c; transform: translateY(-2px); box-shadow: 0 6px 18px rgba(225, 29, 72, 0.38); }}

    /* FAQ Section */
    .faq-box {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 2rem; margin: 3.5rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
    .faq-box h2 {{ font-size: 1.35rem; font-weight: 800; margin-bottom: 1.5rem; border-bottom: 2px solid #0d9488; padding-bottom: 0.5rem; color: #0f172a; }}
    .faq-item {{ margin-bottom: 1.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 1.25rem; }}
    .faq-item:last-child {{ border-bottom: none; margin-bottom: 0; padding-bottom: 0; }}
    .faq-q {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-bottom: 0.6rem; display: flex; gap: 0.5rem; align-items: baseline; }}
    .faq-q span {{ color: #0d9488; font-size: 1.25rem; font-weight: 900; }}
    .faq-a {{ font-size: 0.95rem; color: #475569; line-height: 1.75; padding-left: 1.75rem; }}

    @media (max-width: 640px) {{
      .article-title {{ font-size: 1.45rem; }}
      .rank-card {{ padding: 1.25rem; }}
      .rank-gallery img {{ height: 110px; }}
      .rank-cta-btn {{ width: 100%; justify-content: center; }}
    }}
  </style>

  <!-- Schema.org Article Structured Data -->
  <script type="application/ld+json">
  {article_json_ld}
  </script>

  <!-- Schema.org BreadcrumbList -->
  <script type="application/ld+json">
  {breadcrumb_json_ld}
  </script>

  <!-- Schema.org FAQPage -->
  <script type="application/ld+json">
  {faq_json_ld}
  </script>
</head>
<body>
  <header style="background: #fff; border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 100;">
    <div style="max-width: 1100px; margin: 0 auto; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between;">
      <a href="/" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1.35rem; font-weight: 900; color: #0f172a; letter-spacing: -0.02em;">クラカジ</span>
        <span style="font-size: 0.72rem; background: #0d9488; color: #fff; padding: 2px 8px; border-radius: 9999px; font-weight: 700;">KURAKAJI</span>
      </a>
      <nav style="display: flex; gap: 16px; font-size: 0.88rem; font-weight: 600;">
        <a href="/" style="color: #64748b; text-decoration: none;">ホーム</a>
        <a href="/#editorial" style="color: #64748b; text-decoration: none;">特集一覧</a>
        <a href="/about.html" style="color: #64748b; text-decoration: none;">編集方針</a>
      </nav>
    </div>
  </header>

  <div class="article-container">
    <nav class="breadcrumb-nav">
      <a href="/">ホーム</a>
      <span class="breadcrumb-sep">/</span>
      <a href="/#editorial">{category}</a>
      <span class="breadcrumb-sep">/</span>
      <span>{title}</span>
    </nav>

    <header class="article-header">
      <span class="article-tag">{category}・暮らしの家電検証特集</span>
      <h1 class="article-title">{title}</h1>
      <div class="article-meta">
        <span>最終更新: {updated_at}</span>
        <span>検証執筆: クラカジ 暮らしと家電検証チーム</span>
        <span>掲載数: 厳選{count}選</span>
      </div>
      <div class="article-lead">
        {lead_text}
      </div>
    </header>

    <!-- Buying Guide Section -->
    <section class="guide-box">
      <h2>後悔しないための3つの重要チェックポイント</h2>
      <div class="guide-grid">
        {guide_cards_html}
      </div>
    </section>

    <!-- Comparison Table Section -->
    <div class="compare-table-box">
      <h2>おすすめモデル早見比較表（総合評価順）</h2>
      <table class="styled-table">
        <thead>
          <tr>
            <th>順位</th>
            <th>モデル名</th>
            <th>参考価格</th>
            <th>総合スコア</th>
            <th>詳細</th>
          </tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </div>

    <!-- Product Rankings Detail -->
    <div style="margin: 3.5rem 0 2rem;">
      <h2 style="font-size: 1.55rem; font-weight: 800; color: #0f172a; margin-bottom: 1.75rem; border-left: 5px solid #0d9488; padding-left: 14px;">
        おすすめランキング詳細（厳選{count}アイテム）
      </h2>
      {cards_html}
    </div>

    <!-- FAQ Section -->
    <section class="faq-box">
      <h2>よくある質問（FAQ）</h2>
      {faq_html}
    </section>

    <!-- Editorial Credibility Box -->
    <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-top: 40px;">
      <div style="display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;">
        <div style="flex: 1; min-width: 250px;">
          <h4 style="margin: 0 0 6px 0; font-size: 1.05rem; font-weight: 800; color: #0f172a;">記事執筆・検証：クラカジ 暮らしと家電検証チーム</h4>
          <p style="margin: 0 0 10px 0; font-size: 0.88rem; color: #64748b; line-height: 1.65;">
            一人暮らしの限られた居住空間やタイパ重視の共働き世帯に向けて、楽天市場の売れ筋動向・実機サイズ・消費電力・ユーザー満足度を徹底分析。実用性の高い本当に後悔しない小型家電だけを厳選してご紹介しています。
          </p>
          <div style="font-size: 0.82rem; color: #0284c7; font-weight: 700;">
            <a href="/about.html" style="color: inherit; text-decoration: none;">▶ クラカジの検証基準・編集方針について</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Article Footer CTA -->
    <div class="article-footer-cta" style="margin-top: 45px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #fff; padding: 35px 25px; border-radius: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
      <h3 style="font-size: 1.4rem; font-weight: 800; margin-bottom: 12px; color: #f8fafc;">暮らしをスマートにする家電選びをサポート</h3>
      <p style="font-size: 0.92rem; color: #94a3b8; max-width: 600px; margin: 0 auto 22px; line-height: 1.7;">
        クラカジでは、購入後の「置く場所がない」「結局使わない」を防ぐ実用重視のレビューをお届けしています。
      </p>
      <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
        <a href="/" style="background: #0284c7; color: #fff; padding: 12px 28px; border-radius: 9999px; text-decoration: none; font-weight: 700; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 8px;">
          トップページへ戻る
        </a>
      </div>
    </div>

    <!-- Related Articles -->
    <div style="margin-top: 50px; padding: 28px 24px; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
      <h3 style="font-size: 1.2rem; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 18px; display: flex; align-items: center; gap: 8px;">
        <span style="display: inline-block; width: 4px; height: 18px; background: #0284c7; border-radius: 2px;"></span>
        あわせて読みたい厳選ガイド（おすすめ4選）
      </h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px;">
        <a href="/articles/compact-ceramic-heater-best7.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease;">
          <span style="color: #0284c7; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">🔥 冬の暖房・ヒートショック予防</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">スイッチ2秒で即暖！小型セラミックヒーターおすすめTOP7</span>
        </a>
        <a href="/articles/compact-futon-dryer-best10.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease;">
          <span style="color: #d97706; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">🛌 快眠・ダニ退治</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">冷たい布団を一瞬でホカホカに！小型布団乾燥機TOP10</span>
        </a>
        <a href="/articles/circulator-clothes-drying-best7.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease;">
          <span style="color: #16a34a; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">🌀 部屋干し・節電</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">部屋干し臭ゼロ！サーキュレーターおすすめTOP7</span>
        </a>
        <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="background: #fff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 16px; text-decoration: none; color: inherit; display: block; transition: all 0.2s ease;">
          <span style="color: #dc2626; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 6px;">💡 節電マニュアル</span>
          <span style="font-weight: 700; font-size: 0.92rem; color: #0f172a; line-height: 1.5; display: block;">冬の電気代を月1万円削る小型家電フル活用術</span>
        </a>
      </div>
    </div>
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand-note">
        <strong style="color: #fff; font-size: 1.05rem;">クラカジ (KURAKAJI)</strong>
        <p style="margin-top: 0.4rem; color: #94a3b8; font-size: 0.85rem;">
          暮らしをスマートにする小型家電・生活雑貨家電のセレクトカタログメディア。<br />
          ※当サイトはアフィリエイト広告を利用して商品をご紹介しています。
        </p>
      </div>
      <nav class="footer-nav" aria-label="フッターリンク">
        <a href="/about.html">クラカジについて・編集部紹介</a>
        <a href="/terms.html">利用規約</a>
        <a href="/privacy.html">プライバシーポリシー</a>
      </nav>
      <div class="copyright" style="margin-top: 1.5rem; font-size: 0.78rem; color: #64748b;">
        &copy; 2026 クラカジ (Kurakaji) All Rights Reserved.
      </div>
    </div>
  </footer>

  <aside class="floating-share-bar" aria-label="記事を共有" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; gap: 10px; align-items: center; background: rgba(15,23,42,0.92); backdrop-filter: blur(8px); padding: 8px 14px; border-radius: 9999px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15);">
    <a href="https://bsky.app/intent/compose?text=%E3%82%AF%E3%83%A9%E3%82%AC%E3%82%B8%E3%81%AE%E8%A8%98%E4%BA%8B%E3%82%92%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%EF%BC%81" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #0085ff; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="Blueskyで共有">Bsky</a>
    <a href="https://social-plugins.line.me/lineit/share?url=https%3A%2F%2Fkurakaji.vercel.app" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #06c755; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="LINEで送る">L</a>
    <a href="https://b.hatena.ne.jp/entry/s/kurakaji.vercel.app" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #00a4de; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="はてなブックマークに追加">B!</a>
  </aside>

  <script>
  document.addEventListener('DOMContentLoaded', function() {{
    const progressBar = document.createElement('div');
    progressBar.id = 'reading-progress-bar';
    progressBar.style.cssText = 'position:fixed;top:0;left:0;height:4px;background:linear-gradient(90deg,#0d9488,#f59e0b);width:0%;z-index:99999;transition:width 0.1s ease-out;';
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', function() {{
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (window.pageYOffset / totalHeight) * 100;
      progressBar.style.width = Math.min(100, Math.max(0, progress)) + '%';
    }});

    const container = document.querySelector('.article-container');
    if (container && !document.getElementById('auto-toc-box')) {{
      const headings = container.querySelectorAll('h2');
      if (headings.length >= 3) {{
        const tocBox = document.createElement('nav');
        tocBox.id = 'auto-toc-box';
        tocBox.style.cssText = 'background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:14px;padding:20px 24px;margin:25px 0 35px;box-shadow:0 2px 8px rgba(0,0,0,0.03);';
        let tocHtml = '<div style="display:flex;align-items:center;justify-content:space-between;cursor:pointer;" id="toc-toggle-header">';
        tocHtml += '<span style="font-weight:800;font-size:1.05rem;color:#0f172a;">📑 目次 [タップで開閉]</span>';
        tocHtml += '<span id="toc-arrow" style="font-size:0.85rem;color:#64748b;">▼</span></div>';
        tocHtml += '<ol id="toc-list" style="margin:14px 0 0;padding-left:22px;line-height:1.9;font-size:0.92rem;">';
        headings.forEach((h, idx) => {{
          const id = h.id || 'section-' + (idx + 1);
          h.id = id;
          tocHtml += '<li><a href="#' + id + '" style="color:#0284c7;text-decoration:none;font-weight:600;">' + h.textContent.trim() + '</a></li>';
        }});
        tocHtml += '</ol>';
        tocBox.innerHTML = tocHtml;
        const lead = container.querySelector('.guide-box');
        if (lead) lead.parentNode.insertBefore(tocBox, lead.nextSibling);

        const toggleHeader = document.getElementById('toc-toggle-header');
        const list = document.getElementById('toc-list');
        const arrow = document.getElementById('toc-arrow');
        toggleHeader.addEventListener('click', function() {{
          if (list.style.display === 'none') {{ list.style.display = 'block'; arrow.textContent = '▼'; }}
          else {{ list.style.display = 'none'; arrow.textContent = '▲'; }}
        }});
      }}
    }}
  }});
  </script>
</body>
</html>"""

    os.makedirs(ARTICLES_DIR, exist_ok=True)
    out_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[SUCCESS] 特集HTMLを生成・更新しました: {out_path} ({count}アイテム)")

def check_and_create_monthly_hubs():
    """毎月1日（または月初初回実行時）に新しいハブページを自動で増やすロジック"""
    now = datetime.now()
    current_month = now.month
    monthly_templates = SEASONAL_HUB_TEMPLATES.get(current_month, [])

    created_any = False
    for tmpl in monthly_templates:
        slug = tmpl["slug"]
        hub_json = os.path.join(DATA_DIR, f"{slug}.json")
        if not os.path.exists(hub_json):
            print(f"[MONTHLY HUB] 今月（{current_month}月）の新規ハブページを作成します: {tmpl['title']} ({slug})")
            get_or_create_hub_data(slug, tmpl)
            created_any = True
    return created_any

def re_render_all_hubs():
    """既存の全特集ハブJSONを新テンプレートで再出力"""
    os.makedirs(DATA_DIR, exist_ok=True)
    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json") and f != "posted_item_codes.json"]
    for fname in files:
        slug = fname.replace(".json", "")
        file_path = os.path.join(DATA_DIR, fname)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        render_hub_html(slug, data)

def run_update_cycle():
    """2時間おきの更新サイクル実行"""
    print(f"=== 特集自動更新サイクル開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    # 1. 毎月1日/月初の新規ハブ増設チェック
    check_and_create_monthly_hubs()

    # 2. 既存ハブの中から更新対象を1〜2つ選定（ローテーション）
    posted_cache = get_posted_cache()

    now_month = datetime.now().month
    current_month_slugs = [t["slug"] for t in SEASONAL_HUB_TEMPLATES.get(now_month, [])]
    target_pool = list(set(ACTIVE_FEATURE_SLUGS + current_month_slugs))
    
    chosen_slug = random.choice(target_pool)
    print(f"今回の追加対象特集: [{chosen_slug}]")

    meta_info = find_meta_info(chosen_slug)
    hub_data = get_or_create_hub_data(chosen_slug, meta_info)
    keywords = hub_data.get("keywords", ["小型家電"])
    keyword = random.choice(keywords)
    print(f"検索キーワード: [{keyword}] (ジャンル: {hub_data.get('category')})")

    # 3. 楽天API直接取得
    rakuten_items = fetch_rakuten_items(keyword, hits=20)
    if not rakuten_items:
        print("[WARN] 楽天APIから商品を取得できませんでした。全ハブを再レンダリングして終了します。")
        re_render_all_hubs()
        return

    # 4. 未掲載の商品を1〜2件選別
    existing_codes = set(hub_data.get("posted_codes", []) + [i.get("itemCode") for i in hub_data.get("items", [])])
    candidate = None
    for it in rakuten_items:
        code = it.get("itemCode")
        if code and code not in existing_codes and code not in posted_cache:
            candidate = it
            break

    if not candidate:
        print("[INFO] 全て掲載済みまたはキャッシュ重複のため、最新アイテムを更新モードで再取得")
        candidate = rakuten_items[0]

    # 5. Gemini / AIによるエディトリアル生成
    print(f"AIエディトリアル生成中: {candidate.get('itemName')[:30]}...")
    editorial = generate_product_editorial(
        raw_name=candidate.get("itemName", ""),
        caption=candidate.get("itemCaption", ""),
        price=candidate.get("itemPrice", 0),
        category=hub_data.get("category", "小型家電"),
        rank_num=len(hub_data.get("items", [])) + 1
    )

    candidate.update(editorial)
    print(f"生成完了: スコア {candidate.get('rate')}点 | {candidate.get('clean_name')} | キャッチ: {candidate.get('catchphrase')}")

    # 6. ハブデータへ追加（重複除去しつつrate順ランキングに挿入）
    hub_items = [i for i in hub_data.get("items", []) if i.get("itemCode") != candidate.get("itemCode")]
    hub_items.append(candidate)
    hub_data["items"] = hub_items
    
    # 掲載コード記録
    if "posted_codes" not in hub_data:
        hub_data["posted_codes"] = []
    if candidate.get("itemCode") not in hub_data["posted_codes"]:
        hub_data["posted_codes"].append(candidate.get("itemCode"))
    
    save_hub_data(chosen_slug, hub_data)

    # 7. 全特集HTMLの再レンダリング（新デザイン＆更新適用）
    re_render_all_hubs()

    # 8. キャッシュ保存
    if candidate.get("itemCode") not in posted_cache:
        posted_cache.append(candidate.get("itemCode"))
        save_posted_cache(posted_cache)

    print(f"=== 特集自動更新サイクル完了: {chosen_slug} に商品を追加しました ===")

if __name__ == "__main__":
    if "--re-render-all" in sys.argv:
        re_render_all_hubs()
    else:
        run_update_cycle()
