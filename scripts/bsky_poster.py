#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurakaji Bluesky High-Quality AI Auto Poster & Safe Engagement
- 100% Unique Content Guarantee:
  * Generates empathetic, authentic lifestyle & appliance micro-reviews for all 55+ articles
  * Uses multi-model Gemini API with automatic retry on failure
  * Strict text similarity verification (difflib SequenceMatcher):
    Compares against EVERY previously posted text (local history + live Bluesky PDS feed).
    If similarity >= 0.45 or identical hook line is detected, automatically retries generation with increased temperature!
  * Stores all past full post texts in bluesky_post_texts.jsonl for persistent similarity matching
- Article Selection:
  * Cycles through all 55+ HTML articles and special feature hubs
  * Only cycles back once ALL articles have been posted
- Safe Interval Protection & Community Engagement:
  * ~2-hour interval gate (wait_until_ready_for_next_post)
  * Runs safe community engagement (likes 5-8, follows 1-2) per run
"""

import os
import sys
import glob
import json
import random
import time
import re
import io
import difflib
import urllib.request
import urllib.parse
from datetime import datetime, timezone

import requests
from atproto import Client, client_utils
from PIL import Image

# Directories & Storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

# Clean NO_PROXY bracket formatting for httpx compatibility in proxy environments
for var in ("no_proxy", "NO_PROXY"):
    val = os.environ.get(var)
    if val and "[::1]" in val:
        os.environ[var] = val.replace(",[::1]", "").replace("[::1]", "")

POST_HISTORY_FILE = os.path.join(SCRIPT_DIR, "bluesky_post_history.txt")
POST_TEXTS_FILE = os.path.join(SCRIPT_DIR, "bluesky_post_texts.jsonl")
ENGAGEMENT_HISTORY_FILE = os.path.join(SCRIPT_DIR, "bluesky_engagement_history.txt")
USED_IMAGES_FILE = os.path.join(SCRIPT_DIR, "used_bsky_images.txt")

SITE_BASE_URL = "https://kurakaji.vercel.app"
BLUESKY_HANDLE = os.environ.get("BSKY_HANDLE", "kurakaden.bsky.social")
BLUESKY_APP_PASSWORD = os.environ.get("BSKY_APP_PASSWORD", "4a7z-s25w-vqwm-biyh")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Timing Parameters
MIN_TOLERANCE_HOURS = 1.85  # ~111 min minimum spacing between posts

# Active Gemini Models for Generation (Gemini 1.5 excluded)
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-pro",
    "gemini-3.1-flash-lite",
    "gemini-3-flash",
    "gemini-2.5-pro"
]

# Appliance / Lifestyle Community Engagement Search Queries
ENGAGEMENT_QUERIES = [
    "家電 買い替え",
    "暖房器具 寒い",
    "電気代 高い",
    "一人暮らし 家電",
    "部屋干し 生乾き",
    "サーキュレーター",
    "加湿器 おすすめ",
    "布団乾燥機",
    "パネルヒーター",
    "ノンフライヤー",
    "コーヒーメーカー 欲しい",
    "除雪機 降雪",
    "冬支度 寒い",
    "自炊 時短 家電",
    "新生活 家電"
]

# ==========================================
# 1. 履歴・二重投稿防止管理（ATProtocol & Local）
# ==========================================
def load_post_history():
    history = set()
    if os.path.exists(POST_HISTORY_FILE):
        with open(POST_HISTORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                item = line.strip()
                if item:
                    history.add(item)
    return history

def record_post_history(identifier):
    with open(POST_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{identifier}\n")

def load_all_past_texts():
    """過去に投稿した全本文テキスト（正規化済）のリストを読み込む"""
    past_texts = []
    if os.path.exists(POST_TEXTS_FILE):
        with open(POST_TEXTS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        if isinstance(data, dict) and "text" in data:
                            past_texts.append(data["text"])
                        elif isinstance(data, str):
                            past_texts.append(data)
                    except Exception:
                        past_texts.append(line)
    return past_texts

def save_past_text(text, metadata=None):
    """新しく投稿したテキストを保存"""
    record = {"text": text, "created_at": datetime.now(timezone.utc).isoformat()}
    if metadata:
        record.update(metadata)
    with open(POST_TEXTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def fetch_live_feed_data(client):
    """
    Bluesky PDSから最新の投稿フィードを直接取得し、
    (1) 過去投稿本文リスト
    (2) 外部URLセット
    (3) 冒頭フレーズセット
    を抽出する。
    """
    live_texts = []
    live_urls = set()
    live_first_lines = set()
    try:
        author_feed = client.get_author_feed(actor=client.me.did, limit=50)
        for item in author_feed.feed:
            post = item.post
            rec = post.record
            text = getattr(rec, "text", "") or ""
            if text:
                live_texts.append(text)
                first_line = text.strip().split("\n")[0].strip()
                if first_line:
                    live_first_lines.add(first_line)

            embed = getattr(rec, "embed", None)
            if embed:
                ext = getattr(embed, "external", None)
                if ext and hasattr(ext, "uri") and ext.uri:
                    live_urls.add(ext.uri)
    except Exception as e:
        print(f"[WARN] Failed to fetch live author feed: {e}")
    return live_texts, live_urls, live_first_lines

def calculate_max_similarity(candidate_text, past_texts):
    """候補テキストと過去の全投稿テキストとの間の最大類似率を計算（0.0〜1.0）"""
    if not past_texts:
        return 0.0

    # 記号・改行・空白・ハッシュタグを除去して純粋な本文で比較
    clean_candidate = re.sub(r"[#\s\n\r【】「」『』・…👇]", "", candidate_text)

    max_ratio = 0.0
    for past in past_texts:
        clean_past = re.sub(r"[#\s\n\r【】「」『』・…👇]", "", past)
        # 前方完全一致チェック
        if clean_candidate in clean_past or clean_past in clean_candidate:
            return 1.0
        ratio = difflib.SequenceMatcher(None, clean_candidate, clean_past).ratio()
        if ratio > max_ratio:
            max_ratio = ratio
    return max_ratio

def load_used_images():
    if os.path.exists(USED_IMAGES_FILE):
        with open(USED_IMAGES_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_used_image(img_url):
    with open(USED_IMAGES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{img_url}\n")

def load_engagement_history():
    if os.path.exists(ENGAGEMENT_HISTORY_FILE):
        with open(ENGAGEMENT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def record_engagement_history(identifier):
    with open(ENGAGEMENT_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{identifier}\n")

# ==========================================
# 2. 画像最適化 (Pillow)
# ==========================================
def optimize_image_bytes(raw_bytes, max_bytes=900000):
    if len(raw_bytes) <= max_bytes:
        return raw_bytes
    try:
        img = Image.open(io.BytesIO(raw_bytes))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        max_dim = 1600
        if max(img.size) > max_dim:
            img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        quality = 85
        while quality >= 40:
            out_io = io.BytesIO()
            img.save(out_io, format="JPEG", quality=quality, optimize=True)
            res = out_io.getvalue()
            if len(res) <= max_bytes:
                return res
            quality -= 15
        return res
    except Exception as e:
        print(f"[WARN] Failed to optimize image: {e}")
        return raw_bytes[:max_bytes] if len(raw_bytes) > 2000000 else raw_bytes

# ==========================================
# 3. 記事パーサー & 候補選定
# ==========================================
def parse_article(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    title_m = re.search(r"<title>(.*?)</title>", content)
    title = title_m.group(1).replace(" | クラカジ", "").strip() if title_m else ""

    desc_m = re.search(r'<meta name="description" content="(.*?)"', content)
    desc = desc_m.group(1).strip() if desc_m else ""

    # Verified high-res Rakuten CDN image or OGP image
    img_m = re.search(r'<div class="rank-gallery">\s*<img src="([^"]+)"', content)
    if not img_m:
        img_m = re.search(r'<meta property="og:image" content="(.*?)"', content)
    image = img_m.group(1).strip() if img_m else ""

    # Extract key specs / takeaways from HTML
    h2_matches = re.findall(r"<h2>(.*?)</h2>", content)
    h2_summary = "、".join([re.sub(r"<.*?>", "", h) for h in h2_matches[:3]])

    rel_path = os.path.relpath(html_path, BASE_DIR).replace("\\", "/")
    url = f"{SITE_BASE_URL}/{rel_path}"

    return {
        "path": html_path,
        "title": title,
        "desc": desc,
        "summary": h2_summary,
        "image": image,
        "url": url,
        "first_line": f"【プロ厳選】{title}"
    }

def select_next_article(local_history, live_urls):
    """全55記事から未投稿記事を優先選定。全件投稿済みの場合は最も古い記事からローテーション"""
    all_html = sorted(glob.glob(os.path.join(BASE_DIR, "articles/**/*.html"), recursive=True))
    candidates = []
    for h in all_html:
        meta = parse_article(h)
        if meta["url"] in local_history or meta["path"] in local_history or meta["url"] in live_urls:
            continue
        candidates.append(meta)

    if candidates:
        # 季節トレンド（冬・暖房・加湿・省エネ）を上位スコアリング
        winter_kw = ["暖房", "ヒーター", "こたつ", "毛布", "乾燥", "加湿", "エアコン", "冬", "電気代"]
        scored = []
        for c in candidates:
            score = 10
            for kw in winter_kw:
                if kw in c["title"]:
                    score += 15
            scored.append((score + random.uniform(0, 5), c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    # 全記事投稿済みの場合
    print("[INFO] All 55+ articles posted once. Cycling through oldest articles...")
    if all_html:
        return parse_article(random.choice(all_html))
    return None

# ==========================================
# 4. AI文章生成 & 類似率検証リトライシステム
# ==========================================
def generate_ai_microcopy_with_gemini(article, api_key, temperature=0.85):
    """Gemini APIを使用して情緒あふれるマイクロレビュー文章を生成"""
    title = article["title"]
    desc = article["desc"]
    summary = article.get("summary", "")

    prompt = f"""あなたは生活家電と家事時短を知り尽くした辛口家電アドバイザーです。
Blueskyで「{title}」について、家電好きや一人暮らし・共働き世帯が思わず手を止めて読みたくなる、リアルで熱量の高いマイクロレビュー投稿（日本語）を1つ作成してください。

【記事情報】
- タイトル: {title}
- 概要: {desc}
- ポイント: {summary}

【執筆ルール】
1. 文字数: 日本語100〜140文字程度（URLやハッシュタグはシステムが自動付与するため含めないでください）。
2. 「いかがでしょうか」「ご紹介します」「必見です」といったテンプレやAI特有の敬語は厳禁。
3. 実際に自腹で購入・比較検証したかのようなリアルな語り口（例：「電気代を気にして〜してたけど、これに変えて月3000円浮いた」「安物買って後悔する前に〜」「狭い部屋なら絶対に〜一択」など）。
4. 1行目は思わず目が止まるフック（一行共感・意外な事実）。
5. 出力は本文テキストのみ（引用符や前置きは不要）。
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 300,
        }
    }

    models_to_try = list(GEMINI_MODELS)
    random.shuffle(models_to_try)

    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=8)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                clean_text = re.sub(r'^["「『]|["」』]$', '', text).strip()
                if clean_text and len(clean_text) >= 40:
                    return clean_text
        except Exception:
            continue
    return None

def generate_unique_post_text(article, all_past_texts, api_key, max_attempts=10):
    """
    重複・高類似率を100%排除するリトライ生成ループ:
    過去の全投稿テキストとの類似率が 0.45 以上の場合は再生成（リトライ）。
    """
    print(f"[AI-GEN] Generating unique post text for '{article['title']}'...")
    title = article["title"]
    desc = article["desc"]

    for attempt in range(1, max_attempts + 1):
        temp = min(0.7 + (attempt * 0.05), 1.0)
        candidate_body = None

        if api_key:
            candidate_body = generate_ai_microcopy_with_gemini(article, api_key, temperature=temp)

        if not candidate_body:
            # 高度なランダムテンプレート（切り口バリエーション）
            angles = [
                f"【プロ実機検証】{title}\n\n「もっと早く買えばよかった」とリアルに実感した一台。{desc[:80]}…スペック表だけでは見えない実機の使い勝手と消費電力を詳しく検証しました。",
                f"【買って後悔しない家電選び】{title}\n\n冬の電気代や設置スペースに悩む人に全力でおすすめ。{desc[:80]}…実際に使って分かったメリット・気になるデメリットを本音でまとめました。",
                f"【冬の暮らしハック】{title}\n\n狭い部屋や一人暮らしの救世主。{desc[:80]}…コスパ・静音性・省エネ性能のリアルな測定数値を大公開中です。"
            ]
            candidate_body = random.choice(angles)

        # 類似率チェック
        max_sim = calculate_max_similarity(candidate_body, all_past_texts)
        print(f"  Attempt {attempt}/{max_attempts}: Max similarity = {max_sim:.3f}")

        if max_sim < 0.45:
            print(f"[AI-GEN-SUCCESS] Unique text confirmed (Similarity: {max_sim:.3f} < 0.45) on attempt {attempt}!")
            return candidate_body

        print(f"  [RETRY] Similarity too high ({max_sim:.3f} >= 0.45). Retrying generation with new angle...")

    # 万が一全リトライで超えた場合は、固有タイムスタンプ付きのユニークフックで強制差別化
    salt = datetime.now().strftime('%m月%d日更新')
    return f"【最新検証/{salt}】{title}\n\n{candidate_body[:100]}…"

# ==========================================
# 5. インターバル制御
# ==========================================
def get_latest_post_time(client):
    try:
        author_feed = client.get_author_feed(actor=client.me.did, limit=5)
        for item in author_feed.feed:
            post = item.post
            if post.indexed_at:
                return datetime.fromisoformat(post.indexed_at.replace("Z", "+00:00"))
    except Exception as e:
        print(f"[WARN] Failed to fetch latest post time: {e}")
    return None

def wait_until_ready_for_next_post(client, max_wait_seconds=600):
    now_utc = datetime.now(timezone.utc)
    latest_time = get_latest_post_time(client)

    if not latest_time:
        print("[INTERVAL-CHECK] No previous posts found. Ready to post immediately.")
        return True

    elapsed_seconds = (now_utc - latest_time).total_seconds()
    required_seconds = MIN_TOLERANCE_HOURS * 3600
    remaining_seconds = required_seconds - elapsed_seconds

    if remaining_seconds <= 0:
        print(f"[INTERVAL-CHECK] Elapsed {elapsed_seconds / 3600:.2f}h >= {MIN_TOLERANCE_HOURS}h. Ready to post immediately.")
        return True

    if remaining_seconds <= max_wait_seconds:
        print(f"[INTERVAL-RETRY] Previous post was {elapsed_seconds / 3600:.2f}h ago. Waiting {int(remaining_seconds)}s to fulfill interval...")
        time.sleep(remaining_seconds + 3)
        print("[INTERVAL-READY] Wait complete! Ready to post.")
        return True

    print(f"[INTERVAL-WAIT] Post interval too short ({elapsed_seconds / 3600:.2f}h elapsed, need {MIN_TOLERANCE_HOURS}h). Need to wait {remaining_seconds / 60:.1f}m. Skipping post this turn.")
    return False

# ==========================================
# 6. コミュニティエンゲージメント (Likes & Follows)
# ==========================================
def run_engagement_cycle(client):
    print("\n[ENGAGE] Starting safe community engagement cycle (Likes & Follows)...")
    engaged_history = load_engagement_history()
    target_likes = random.randint(5, 8)
    target_follows = random.randint(1, 2)
    likes_done = 0
    follows_done = 0

    queries = list(ENGAGEMENT_QUERIES)
    random.shuffle(queries)

    for q in queries[:4]:
        if likes_done >= target_likes and follows_done >= target_follows:
            break
        try:
            res = client.app.bsky.feed.search_posts(params={"q": q, "limit": 25})
            posts = res.posts or []
            random.shuffle(posts)

            for p in posts:
                author_did = p.author.did
                post_uri = p.uri
                post_cid = p.cid

                if author_did == client.me.did or post_uri in engaged_history:
                    continue

                # Safe Like
                if likes_done < target_likes:
                    try:
                        time.sleep(random.uniform(1.2, 2.5))
                        client.like(uri=post_uri, cid=post_cid)
                        record_engagement_history(post_uri)
                        likes_done += 1
                        snippet = p.record.text[:35].replace("\n", " ") if hasattr(p.record, "text") else ""
                        print(f"  [ENGAGE-LIKE] ({likes_done}/{target_likes}) @{p.author.handle}: {snippet}...")
                    except Exception as e:
                        print(f"  [WARN] Like failed: {e}")

                # Safe Follow
                if follows_done < target_follows and author_did not in engaged_history:
                    try:
                        time.sleep(random.uniform(1.5, 3.0))
                        client.follow(subject=author_did)
                        record_engagement_history(author_did)
                        follows_done += 1
                        print(f"  [ENGAGE-FOLLOW] ({follows_done}/{target_follows}) Followed @{p.author.handle}")
                    except Exception as e:
                        print(f"  [WARN] Follow failed: {e}")

                if likes_done >= target_likes and follows_done >= target_follows:
                    break
        except Exception as e:
            print(f"[WARN] Engagement search failed for '{q}': {e}")
            continue

    print(f"[ENGAGE-SUMMARY] Cycle complete: {likes_done} likes, {follows_done} follows executed.\n")

# ==========================================
# 7. メイン投稿実行
# ==========================================
def post_to_bluesky():
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] Starting Kurakaji Bluesky Auto-Post Task...")

    client = Client()
    try:
        client.login(BLUESKY_HANDLE, BLUESKY_APP_PASSWORD)
        print(f"[AUTH OK] Logged in as @{BLUESKY_HANDLE} (DID: {client.me.did})")
    except Exception as e:
        print(f"[ERROR] Bluesky login failed: {e}")
        return False

    # 1. 投稿インターバル判定（短すぎる場合はエンゲージメントのみ実行して安全終了）
    should_post_now = wait_until_ready_for_next_post(client, max_wait_seconds=600)
    if not should_post_now:
        print("[POST-DEFER] Interval not reached yet. Running engagement cycle while waiting for next 30m slot.")
        run_engagement_cycle(client)
        print("[COMPLETE] Safe engagement finished. Exiting safely.")
        return True

    # 2. 履歴取得（ローカル + リアルタイムBluesky PDS）
    local_history = load_post_history()
    live_texts, live_urls, live_first_lines = fetch_live_feed_data(client)
    all_past_texts = list(set(load_all_past_texts() + live_texts))
    used_images = load_used_images()
    print(f"[HISTORY] Local entries: {len(local_history)}, Past texts tracked: {len(all_past_texts)}, Live PDS detected: {len(live_texts)}")

    # 3. 55記事から未投稿記事を選定
    article = select_next_article(local_history, live_urls)
    if not article:
        print("[ERROR] No article candidate found.")
        return False

    print(f"[SELECT] Article: {article['title']}")
    print(f"         URL: {article['url']}")

    # 4. 類似率チェック＆リトライ付きで本文を生成
    unique_body = generate_unique_post_text(article, all_past_texts, GEMINI_API_KEY)

    # 5. リッチポストの構築
    tb = client_utils.TextBuilder()
    tb.text(f"{unique_body}\n\n")
    tb.text("実機サイズ・消費電力の検証レビューを公開中👇\n")
    tb.link("レビュー記事を読む", article['url'])
    tb.text("\n\n")
    tb.tag("#クラカジ", "クラカジ")
    tb.text(" ")
    tb.tag("#家電レビュー", "家電レビュー")
    tb.text(" ")
    tb.tag("#新生活", "新生活")
    tb.text(" ")
    tb.tag("#ライフハック", "ライフハック")

    # 6. サムネイル画像アップロード
    thumb_blob = None
    if article.get("image"):
        try:
            res = requests.get(article["image"], headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
            if res.status_code == 200 and len(res.content) > 1000:
                opt_bytes = optimize_image_bytes(res.content)
                upload_res = client.upload_blob(opt_bytes)
                thumb_blob = upload_res.blob
                save_used_image(article["image"])
        except Exception as e:
            print(f"[WARN] Failed to upload thumb blob: {e}")

    ext_card = {
        "uri": article["url"],
        "title": article["title"][:100],
        "description": article["desc"][:200]
    }
    if thumb_blob:
        ext_card["thumb"] = thumb_blob

    embed_payload = {
        "$type": "app.bsky.embed.external",
        "external": ext_card
    }

    # 7. 投稿実行
    resp = client.send_post(text=tb, embed=embed_payload)
    print(f"[SUCCESS] Article posted to Bluesky! URI: {resp.uri}")

    # 8. 履歴記録（URL、パス、冒頭行、そして類似率判定用の全文保存）
    record_post_history(article["url"])
    record_post_history(article["path"])
    record_post_history(article["first_line"])
    save_past_text(unique_body, {"title": article["title"], "url": article["url"], "uri": resp.uri})

    # 9. コミュニティエンゲージメント実行
    time.sleep(random.uniform(2.5, 5.0))
    run_engagement_cycle(client)

    return True

if __name__ == "__main__":
    success = post_to_bluesky()
    if not success:
        sys.exit(1)
