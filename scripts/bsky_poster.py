#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kurakaji Bluesky High-Quality Auto Poster & Safe Engagement
Modeled after production croud-travel architecture:
- 1:1 alternating posting strategy:
  * Mode "article": Official rich link embed card with authentic Rakuten high-res image & verified specs
  * Mode "trivia": High-engagement linkless viral appliance tip / trivia with curated high-res imagery
- Strict multi-layer deduplication:
  1. Live ATProtocol feed scan (queries Bluesky PDS directly)
  2. Local persistent history file (bluesky_post_history.txt)
  3. Text similarity & URL hash checking
  => Absolutely prevents duplicate content from ever being posted!
- Interval Protection:
  * Strict interval gating (wait_until_ready_for_next_post) to keep account safe
  * Runs safe community engagement (likes 5-8, follows 1-2) on every execution
"""

import os
import sys
import glob
import json
import random
import time
import re
import io
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
ENGAGEMENT_HISTORY_FILE = os.path.join(SCRIPT_DIR, "bluesky_engagement_history.txt")
USED_IMAGES_FILE = os.path.join(SCRIPT_DIR, "used_bsky_images.txt")

SITE_BASE_URL = "https://kurakaji.vercel.app"
BLUESKY_HANDLE = os.environ.get("BSKY_HANDLE", "kurakaden.bsky.social")
BLUESKY_APP_PASSWORD = os.environ.get("BSKY_APP_PASSWORD", "4a7z-s25w-vqwm-biyh")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Timing Parameters (30-min cron trigger with 2-hour interval gate)
MIN_TOLERANCE_HOURS = 1.85  # ~111 min minimum spacing between posts

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

# Curated High-Engagement Lifestyle & Appliance Trivia Master Pool
VIRAL_TRIVIA_LIST = [
    {
        "id": "trivia_heater_cost",
        "topic": "セラミックヒーターとエアコン電気代",
        "text": """【知らなきゃ大損する冬の暖房トリビア】

「足元が寒いから」と小型セラミックファンヒーターをデスク下で1日8時間つけっぱなしにしてる人、実はエアコン暖房より電気代高いです。

・エアコン暖房：約 5,200円/月
・セラミックヒーター：約 8,200円/月 ⚠️

セラミックは1200W食うので1時間37円。
足元だけなら190W（1時間5円・月1200円）の「5面パネルヒーター」にするだけで月7,000円浮きます。

#家電豆知識 #節電 #電気代 #ライフハック #暮らしの知恵""",
        "images": [
            ("https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=800&auto=format&fit=crop&q=80", "冬の暖かなリビング照明"),
            ("https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=80", "温かみのある北欧風の部屋"),
            ("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop&q=80", "快適な温度に保たれたデスクスペース")
        ]
    },
    {
        "id": "trivia_room_drying",
        "topic": "部屋干し生乾き臭防止ルール",
        "text": """【雨の日の部屋干し臭を100%防ぐ干し方】

洗濯物の「生乾き臭」の原因菌モラクセラは、濡れた状態が【5時間】続くと爆発的に繁殖します。

臭わせない黄金ルール：
① 洗濯物同士の間隔はこぶし1個分（約10cm）空ける
② アーチ干し（長い服を両端、短い服を中央）で空気の通り道を作る
③ サーキュレーターの風を真下から斜め上へ送る

これで乾くスピードが3倍になります。

#部屋干し #洗濯 #サーキュレーター #暮らしの知恵 #家事ハック""",
        "images": [
            ("https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&auto=format&fit=crop&q=80", "清潔に干された洗濯物"),
            ("https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=800&auto=format&fit=crop&q=80", "明るいサンルームとリネン"),
            ("https://images.unsplash.com/photo-1489274495757-95c7c837b101?w=800&auto=format&fit=crop&q=80", "自然光が差し込む洗濯スペース")
        ]
    },
    {
        "id": "trivia_kotatsu_saving",
        "topic": "一人暮らしの着るこたつ省エネ",
        "text": """【一人暮らし最強の冬暖房は『着るこたつ』】

冬の暖房代を極限まで削りたいなら、一人用こたつや電気着る毛布が圧倒的です。

・エアコン暖房：約 5,200円/月
・オイルヒーター：約 14,000円/月
・一人用こたつ：約 1,100円/月
・USB着る電気ブランケット：約 180円/月 ⚡️

空間全体を温めず、身体だけを直温めするのが一番賢い節約術です。

#一人暮らし #こたつ #省エネ #防寒グッズ #冬支度""",
        "images": [
            ("https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&auto=format&fit=crop&q=80", "ぬくもりある冬のブランケット"),
            ("https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=800&auto=format&fit=crop&q=80", "リラックスできる北欧インテリア"),
            ("https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=800&auto=format&fit=crop&q=80", "温かなコーヒーと冬の室内")
        ]
    },
    {
        "id": "trivia_futon_dani",
        "topic": "布団乾燥機ダニ死滅の温度と時間",
        "text": """【天日干しではダニは死なない事実】

天気の良い日に布団を干しても、ダニは温度の低い裏側へ逃げるだけなのでほぼ死滅しません。

ダニ退治の科学的条件：
・50℃以上で20分〜30分
・60℃以上なら一瞬で死滅

布団乾燥機の「ダニ退治モード（約65℃で100分）」をかけた後、死骸を掃除機でしっかり吸引するのが唯一の正解です。

#布団乾燥機 #アレルギー対策 #ダニ退治 #快眠 #家事ハック""",
        "images": [
            ("https://images.unsplash.com/photo-1616046229478-9901c5536a45?w=800&auto=format&fit=crop&q=80", "清潔でふかふかなベッドルーム"),
            ("https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&auto=format&fit=crop&q=80", "心地よい寝具と自然光"),
            ("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800&auto=format&fit=crop&q=80", "温かみのあるモダン寝室")
        ]
    },
    {
        "id": "trivia_humidifier_placement",
        "topic": "加湿器の正しい置き場所",
        "text": """【加湿器を窓際や床に直置きしてはいけない理由】

加湿器を窓際に置くと、冷気で冷やされて結露（カビの原因）になるだけで部屋が潤いません。
また、床直置きだとセンサーが「室温が低い＝湿度が高い」と誤認して弱運転になってしまいます。

正解の置き場所：
① 床から70cm〜100cmの高さ（デスクや棚の上）
② エアコンの風が当たる場所（風に乗って部屋全体に拡散）

#加湿器 #乾燥対策 #インフルエンザ予防 #冬の暮らし""",
        "images": [
            ("https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=80", "潤いのある心地よいリビング"),
            ("https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?w=800&auto=format&fit=crop&q=80", "すっきり片付いたデスク周り")
        ]
    },
    {
        "id": "trivia_airfryer_healthy",
        "topic": "ノンフライヤーで脂質85%カット",
        "text": """【揚げ物好きの一人暮らしは全員ノンフライヤー買うべき】

ノンフライヤーの真価は「油を使わずに揚げられる」だけじゃありません。

市販の冷めたお惣菜（唐揚げ・天ぷら）を温め直すと、余計な油が下にゴッソリ落ちて脂質最大85%カット。しかも衣は揚げたて以上にサックサクに蘇ります。

油ハネも火災の心配もゼロ、食洗機で丸洗いできるので自炊の時短革命が起きます。

#ノンフライヤー #ヘルシーレシピ #時短料理 #自炊男子 #一人暮らし""",
        "images": [
            ("https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=800&auto=format&fit=crop&q=80", "清潔感あふれる最新キッチン"),
            ("https://images.unsplash.com/photo-1507089947368-19c1da9775ae?w=800&auto=format&fit=crop&q=80", "手軽に美味しいおうちご飯")
        ]
    }
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

def fetch_live_feed_identifiers(client):
    """
    Bluesky PDSから最新の投稿フィードを直接取得し、
    過去に投稿した本文冒頭フレーズや外部URLをセットとして抽出する。
    """
    live_ids = set()
    try:
        author_feed = client.get_author_feed(actor=client.me.did, limit=50)
        for item in author_feed.feed:
            post = item.post
            rec = post.record
            text = getattr(rec, "text", "") or ""
            # Extract first line / hook
            first_line = text.strip().split("\n")[0].strip()
            if first_line:
                live_ids.add(first_line)

            # Extract external embed card URL
            embed = getattr(rec, "embed", None)
            if embed:
                ext = getattr(embed, "external", None)
                if ext and hasattr(ext, "uri") and ext.uri:
                    live_ids.add(ext.uri)
    except Exception as e:
        print(f"[WARN] Failed to fetch live author feed: {e}")
    return live_ids

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

    rel_path = os.path.relpath(html_path, BASE_DIR).replace("\\", "/")
    url = f"{SITE_BASE_URL}/{rel_path}"

    return {
        "path": html_path,
        "title": title,
        "desc": desc,
        "image": image,
        "url": url,
        "first_line": f"【プロ厳選】{title}"
    }

def select_unposted_article(local_history, live_history):
    all_html = sorted(glob.glob(os.path.join(BASE_DIR, "articles/**/*.html"), recursive=True))
    candidates = []
    for h in all_html:
        meta = parse_article(h)
        # Check against both local history and live feed history
        if meta["url"] in local_history or meta["path"] in local_history:
            continue
        if meta["url"] in live_history or meta["first_line"] in live_history:
            continue
        candidates.append(meta)

    if candidates:
        # Prioritize winter/heating/seasonal topics in Nov-Feb
        winter_kw = ["暖房", "ヒーター", "こたつ", "毛布", "乾燥", "加湿", "エアコン", "冬"]
        scored = []
        for c in candidates:
            score = 10
            for kw in winter_kw:
                if kw in c["title"]:
                    score += 15
            scored.append((score + random.uniform(0, 5), c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    # If all published, loop back safely
    print("[INFO] All articles posted once. Cycling through oldest articles...")
    if all_html:
        return parse_article(random.choice(all_html))
    return None

def select_unposted_trivia(local_history, live_history):
    candidates = []
    for t in VIRAL_TRIVIA_LIST:
        first_line = t["text"].strip().split("\n")[0].strip()
        if t["id"] in local_history or first_line in live_history:
            continue
        candidates.append(t)

    if candidates:
        return random.choice(candidates)

    print("[INFO] All trivia posted once. Selecting least recently used trivia...")
    return random.choice(VIRAL_TRIVIA_LIST)

# ==========================================
# 4. インターバル制御 & 判定
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
# 5. コミュニティエンゲージメント (Likes & Follows)
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
# 6. メイン投稿実行
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
    live_history = fetch_live_feed_identifiers(client)
    used_images = load_used_images()
    print(f"[HISTORY] Local entries: {len(local_history)}, Live PDS detected: {len(live_history)}")

    # 3. 投稿モード判定 (交互: 偶数回=記事カード, 奇数回=バズトリビア)
    post_count = len(local_history)
    mode = "trivia" if (post_count % 2 == 1) else "article"
    print(f"[MODE] Current mode: {mode.upper()} (Total past posts: {post_count})")

    if mode == "article":
        article = select_unposted_article(local_history, live_history)
        if not article:
            print("[ERROR] No article candidate found.")
            return False

        print(f"[SELECT] Article: {article['title']}")
        print(f"         URL: {article['url']}")

        # Build Rich Post Text
        tb = client_utils.TextBuilder()
        tb.text(f"【プロ厳選】{article['title']}\n\n")
        tb.text(f"{article['desc'][:110]}…\n\n")
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

        # Upload External Embed Thumbnail
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

        # Post Record with External Card Embed
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

        resp = client.send_post(text=tb, embed=embed_payload)
        print(f"[SUCCESS] Article posted to Bluesky! URI: {resp.uri}")

        record_post_history(article["url"])
        record_post_history(article["path"])
        record_post_history(article["first_line"])

    else:
        # Trivia Mode
        trivia = select_unposted_trivia(local_history, live_history)
        print(f"[SELECT] Trivia Topic: {trivia['topic']}")

        tb = client_utils.TextBuilder()
        tb.text(trivia["text"])

        # Pick unique image
        selected_img = None
        selected_alt = "暮らしと家電の知恵"
        for u, alt in trivia.get("images", []):
            if u not in used_images:
                selected_img = u
                selected_alt = alt
                break
        if not selected_img and trivia.get("images"):
            selected_img, selected_alt = random.choice(trivia["images"])

        uploaded_img_blob = None
        if selected_img:
            try:
                res = requests.get(selected_img, headers={"User-Agent": "Mozilla/5.0"}, timeout=12)
                if res.status_code == 200 and len(res.content) > 1000:
                    opt_bytes = optimize_image_bytes(res.content)
                    uploaded_img_blob = client.upload_blob(opt_bytes)
                    save_used_image(selected_img)
            except Exception as e:
                print(f"[WARN] Failed to upload trivia image blob: {e}")

        if uploaded_img_blob:
            resp = client.send_image(
                text=tb,
                image=opt_bytes,
                image_alt=selected_alt
            )
            print(f"[SUCCESS] Trivia posted with image! URI: {resp.uri}")
        else:
            resp = client.send_post(text=tb)
            print(f"[SUCCESS] Trivia posted (text only)! URI: {resp.uri}")

        first_line = trivia["text"].strip().split("\n")[0].strip()
        record_post_history(trivia["id"])
        record_post_history(first_line)

    # 4. ポスト後のコミュニティエンゲージメント実行
    time.sleep(random.uniform(2.5, 5.0))
    run_engagement_cycle(client)

    return True

if __name__ == "__main__":
    success = post_to_bluesky()
    if not success:
        sys.exit(1)
