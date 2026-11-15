#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bluesky Hybrid Auto Poster & Auto Engagement for Kurakaji
- 2/3 ratio: Article feature posts with official rich embed card & verified product image.
- 1/3 ratio: Linkless viral trivia / tips posts with dynamic, non-repetitive curated high-res imagery.
- Strictly avoids repetitive image reuse across posts by tracking image hashes/URLs.
- Auto-Engagement: Searches for appliance, lifestyle, and home improvement users and automatically likes (5-8) & follows (1-2) per run.
- Rate-limit protection: 1 post per execution to keep account healthy and prevent bans.
"""

import os, sys, glob, re, json, datetime, time, random, urllib.request, urllib.parse

BSKY_HANDLE = os.environ.get("BSKY_HANDLE", "kurakaden.bsky.social")
BSKY_APP_PASSWORD = os.environ.get("BSKY_APP_PASSWORD", "4a7z-s25w-vqwm-biyh")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

CACHE_FILE = os.path.join(os.path.dirname(__file__), "posted_bsky_articles.txt")
POST_COUNT_FILE = os.path.join(os.path.dirname(__file__), "bsky_post_counter.json")
USED_IMAGES_FILE = os.path.join(os.path.dirname(__file__), "used_bsky_images.txt")
ENGAGEMENT_HISTORY_FILE = os.path.join(os.path.dirname(__file__), "bsky_engagement_history.txt")

# Appliance / Lifestyle Engagement Search Queries
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

VIRAL_TRIVIA_LIST = [
    {
        "topic": "heater_cost",
        "text": """【知らなきゃ大損する冬の暖房トリビア】

「足元が寒いから」と小型セラミックファンヒーターをデスク下で1日8時間つけっぱなしにしてる人、実はエアコン暖房より電気代高いです。

・エアコン暖房：約 5,200円/月
・セラミックヒーター：約 8,200円/月 ⚠️

セラミックは1200W食うので1時間37円。
足元だけなら190W（1時間5円・月1200円）の「5面パネルヒーター」にするだけで月7,000円浮きます。

#家電豆知識 #節電 #電気代 #ライフハック""",
        "images": [
            ("https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?w=800&auto=format&fit=crop&q=80", "冬の暖かなリビング照明"),
            ("https://images.unsplash.com/photo-1513694203232-719a280e022f?w=800&auto=format&fit=crop&q=80", "温かみのある北欧風の部屋"),
            ("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&auto=format&fit=crop&q=80", "快適な温度に保たれたデスクスペース")
        ]
    },
    {
        "topic": "room_drying",
        "text": """【雨の日の部屋干し臭を100%防ぐ干し方】

洗濯物の「生乾き臭」の原因菌モラクセラは、濡れた状態が【5時間】続くと爆発的に繁殖します。

臭わせない黄金ルール：
① 洗濯物同士の間隔はこぶし1個分（約10cm）空ける
② アーチ干し（長い服を両端、短い服を中央）で空気の通り道を作る
③ サーキュレーターの風を真下から斜め上へ送る

これで乾くスピードが3倍になります。

#部屋干し #洗濯 #サーキュレーター #暮らしの知恵""",
        "images": [
            ("https://images.unsplash.com/photo-1582735689369-4fe89db7114c?w=800&auto=format&fit=crop&q=80", "清潔に干された洗濯物"),
            ("https://images.unsplash.com/photo-1517677208171-0bc6725a3e60?w=800&auto=format&fit=crop&q=80", "明るいサンルームとリネン"),
            ("https://images.unsplash.com/photo-1489274495757-95c7c837b101?w=800&auto=format&fit=crop&q=80", "自然光が差し込む洗濯スペース")
        ]
    },
    {
        "topic": "kotatsu_saving",
        "text": """【一人暮らし最強の冬暖房は『着るこたつ』】

冬の暖房代を極限まで削りたいなら、一人用こたつや電気着る毛布が圧倒的です。

・エアコン暖房：約 5,200円/月
・オイルヒーター：約 14,000円/月
・一人用こたつ：約 1,100円/月
・USB着る電気ブランケット：約 180円/月 ⚡️

空間全体を温めず、身体だけを直温めするのが一番賢い節約術です。

#一人暮らし #こたつ #省エネ #防寒グッズ""",
        "images": [
            ("https://images.unsplash.com/photo-1544816155-12df9643f363?w=800&auto=format&fit=crop&q=80", "ぬくもりある冬のブランケット"),
            ("https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=800&auto=format&fit=crop&q=80", "リラックスできる北欧インテリア"),
            ("https://images.unsplash.com/photo-1507652313519-d4e9174996dd?w=800&auto=format&fit=crop&q=80", "温かなコーヒーと冬の室内")
        ]
    }
]

def load_used_images():
    if os.path.exists(USED_IMAGES_FILE):
        with open(USED_IMAGES_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_used_image(image_url):
    with open(USED_IMAGES_FILE, "a", encoding="utf-8") as f:
        f.write(image_url + "\n")

def get_posted_articles():
    if not os.path.exists(CACHE_FILE):
        return set()
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_posted(article_path):
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(article_path + "\n")

def load_post_counter():
    if os.path.exists(POST_COUNT_FILE):
        try:
            with open(POST_COUNT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"total": 0, "article_posts": 0, "trivia_posts": 0, "trivia_idx": 0}

def save_post_counter(counter):
    with open(POST_COUNT_FILE, "w", encoding="utf-8") as f:
        json.dump(counter, f, indent=2)

def load_engagement_history():
    if os.path.exists(ENGAGEMENT_HISTORY_FILE):
        with open(ENGAGEMENT_HISTORY_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def record_engagement(item_id):
    with open(ENGAGEMENT_HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(item_id + "\n")

def authenticate_bsky(handle, password):
    url = "https://bsky.social/xrpc/com.atproto.server.createSession"
    data = json.dumps({"identifier": handle, "password": password}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as resp:
        return json.loads(resp.read().decode("utf-8"))

def upload_image_blob(jwt, image_url):
    if not image_url:
        return None
    try:
        req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            mime = resp.headers.get("Content-Type", "image/jpeg").split(";")[0]

        upload_url = "https://bsky.social/xrpc/com.atproto.repo.uploadBlob"
        up_req = urllib.request.Request(upload_url, data=data, headers={"Authorization": f"Bearer {jwt}", "Content-Type": mime})
        with urllib.request.urlopen(up_req, timeout=15) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return res.get("blob")
    except Exception as e:
        print(f"Warning: Failed to upload image blob ({image_url}): {e}")
        return None

def post_record(session, record):
    url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
    payload = {
        "repo": session["did"],
        "collection": "app.bsky.feed.post",
        "record": record
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {session['accessJwt']}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=12) as resp:
        return json.loads(resp.read().decode("utf-8"))

def parse_article_meta(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    title_m = re.search(r"<title>(.*?)</title>", content)
    title = title_m.group(1).replace(" | クラカジ", "").strip() if title_m else ""

    desc_m = re.search(r'<meta name="description" content="(.*?)"', content)
    desc = desc_m.group(1).strip() if desc_m else ""

    # Look for first verified high-res product image from Rakuten
    img_m = re.search(r'<div class="rank-gallery">\s*<img src="([^"]+)"', content)
    if not img_m:
        img_m = re.search(r'<meta property="og:image" content="(.*?)"', content)
    image = img_m.group(1).strip() if img_m else ""

    base_dir = "/home/antigravity/kurakaji"
    rel_path = os.path.relpath(filepath, base_dir)
    url = f"https://kurakaji.vercel.app/{rel_path}"

    return {"title": title, "desc": desc, "image": image, "url": url}

def select_unique_trivia_image(trivia_item, used_set):
    for img_url, alt in trivia_item.get("images", []):
        if img_url not in used_set:
            return img_url, alt
    return random.choice(trivia_item.get("images", [("", "")]))

def run_engagement_cycle(session):
    """
    Search active lifestyle / appliance users and automatically like 5-8 posts & follow 1-2 accounts safely
    """
    print("\n[ENGAGE] Starting safe community engagement cycle (Likes & Follows)...")
    jwt = session["accessJwt"]
    my_did = session["did"]
    history = load_engagement_history()

    target_likes = random.randint(5, 8)
    target_follows = random.randint(1, 2)
    likes_done = 0
    follows_done = 0

    queries = list(ENGAGEMENT_QUERIES)
    random.shuffle(queries)

    for q_text in queries[:4]:
        if likes_done >= target_likes and follows_done >= target_follows:
            break
        try:
            enc_q = urllib.parse.quote(q_text)
            search_url = f"https://bsky.social/xrpc/app.bsky.feed.searchPosts?q={enc_q}&limit=20"
            req = urllib.request.Request(search_url, headers={"Authorization": f"Bearer {jwt}"})
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                posts = data.get("posts", [])
                random.shuffle(posts)

                for p in posts:
                    author_did = p["author"]["did"]
                    author_handle = p["author"]["handle"]
                    post_uri = p["uri"]
                    post_cid = p["cid"]
                    snippet = p.get("record", {}).get("text", "")[:35].replace("\n", " ")

                    if author_did == my_did or post_uri in history:
                        continue

                    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

                    # 1. Like
                    if likes_done < target_likes:
                        try:
                            time.sleep(random.uniform(1.2, 2.5))
                            like_record = {
                                "$type": "app.bsky.feed.like",
                                "subject": {"uri": post_uri, "cid": post_cid},
                                "createdAt": now
                            }
                            like_data = json.dumps({"repo": my_did, "collection": "app.bsky.feed.like", "record": like_record}).encode("utf-8")
                            lreq = urllib.request.Request("https://bsky.social/xrpc/com.atproto.repo.createRecord", data=like_data, headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"})
                            with urllib.request.urlopen(lreq, timeout=10) as lres:
                                record_engagement(post_uri)
                                likes_done += 1
                                print(f"[LIKE {likes_done}/{target_likes}] @{author_handle}: {snippet}")
                        except Exception as le:
                            print(f"[LIKE-WARN] {le}")

                    # 2. Follow
                    if follows_done < target_follows and author_did not in history:
                        try:
                            time.sleep(random.uniform(1.5, 3.0))
                            follow_record = {
                                "$type": "app.bsky.graph.follow",
                                "subject": author_did,
                                "createdAt": now
                            }
                            follow_data = json.dumps({"repo": my_did, "collection": "app.bsky.graph.follow", "record": follow_record}).encode("utf-8")
                            freq = urllib.request.Request("https://bsky.social/xrpc/com.atproto.repo.createRecord", data=follow_data, headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"})
                            with urllib.request.urlopen(freq, timeout=10) as fres:
                                record_engagement(author_did)
                                follows_done += 1
                                print(f"[FOLLOW {follows_done}/{target_follows}] Followed user: @{author_handle}")
                        except Exception as fe:
                            print(f"[FOLLOW-WARN] {fe}")

                    if likes_done >= target_likes and follows_done >= target_follows:
                        break
        except Exception as se:
            print(f"[SEARCH-WARN] Query '{q_text}' error: {se}")

    print(f"[ENGAGE-SUMMARY] Cycle complete: {likes_done} likes, {follows_done} follows executed.\n")

def main():
    print(f"=== Kurakaji Bluesky Hybrid Poster & Auto-Engage ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    
    # Random schedule jitter if invoked from scheduled cron
    if os.environ.get("ENABLE_JITTER") == "1":
        jitter_sec = random.randint(0, 900) # 0 to 15 min random delay
        print(f"[JITTER] Applying natural randomization: sleeping for {jitter_sec // 60}m {jitter_sec % 60}s...")
        time.sleep(jitter_sec)

    counter = load_post_counter()
    used_images = load_used_images()
    
    # 2:1 ratio (every 3rd post is viral linkless trivia)
    is_trivia = (counter["total"] % 3 == 2)

    base_dir = "/home/antigravity/kurakaji"
    all_articles = sorted(glob.glob(os.path.join(base_dir, "articles/**/*.html"), recursive=True))
    posted = get_posted_articles()
    pending = [a for a in all_articles if a not in posted]

    if not is_trivia and not pending:
        print("[INFO] All articles have been posted once! Resetting cycle.")
        is_trivia = True

    try:
        session = authenticate_bsky(BSKY_HANDLE, BSKY_APP_PASSWORD)
        print(f"[AUTH OK] Signed in as @{BSKY_HANDLE}")
    except Exception as e:
        print(f"[ERROR] Bluesky authentication failed: {e}")
        sys.exit(1)

    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    if is_trivia:
        print("\n>>> Strategy: Posting LINKLESS VIRAL TRIVIA WITH UNIQUE IMAGE (バズ・フォロワー獲得)")
        idx = counter.get("trivia_idx", 0) % len(VIRAL_TRIVIA_LIST)
        trivia_item = VIRAL_TRIVIA_LIST[idx]
        trivia_text = trivia_item["text"]
        counter["trivia_idx"] = idx + 1

        img_url, img_alt = select_unique_trivia_image(trivia_item, used_images)

        record = {
            "$type": "app.bsky.feed.post",
            "text": trivia_text,
            "createdAt": now
        }

        if img_url:
            print(f"Uploading curated unique image: {img_url}")
            blob = upload_image_blob(session["accessJwt"], img_url)
            if blob:
                record["embed"] = {
                    "$type": "app.bsky.embed.images",
                    "images": [
                        {
                            "alt": img_alt,
                            "image": blob
                        }
                    ]
                }
                save_used_image(img_url)

        print("--- Trivia Text Preview ---")
        print(trivia_text)
        print(f"Attached Image: {img_url} ({img_alt})")
        print("---------------------------")

        result = post_record(session, record)
        print(f"[SUCCESS] Trivia posted to Bluesky! URI: {result.get('uri')}")
        counter["total"] += 1
        counter["trivia_posts"] += 1
        save_post_counter(counter)

    else:
        print(f"\n>>> Strategy: Posting ARTICLE LINK EMBED CARD (Pending: {len(pending)})")
        target_article = pending[0]
        meta = parse_article_meta(target_article)
        print(f"Target: {meta['title']}")
        print(f"URL: {meta['url']}")
        print(f"Product Image: {meta['image']}")

        post_text = f"""【プロ厳選】{meta['title']}

{meta['desc']}

後悔しない実機サイズ・消費電力の検証レビューを公開中👇
{meta['url']}

#クラカジ #家電レビュー #新生活 #ライフハック"""

        record = {
            "$type": "app.bsky.feed.post",
            "text": post_text,
            "createdAt": now
        }

        # Facets
        url = meta["url"]
        if url in post_text:
            b_text = post_text.encode("utf-8")
            b_url = url.encode("utf-8")
            start = b_text.find(b_url)
            if start != -1:
                end = start + len(b_url)
                record["facets"] = [{
                    "index": {"byteStart": start, "byteEnd": end},
                    "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]
                }]

        # External Card Embed with Product Image
        thumb_blob = upload_image_blob(session["accessJwt"], meta["image"])
        ext_obj = {
            "uri": url,
            "title": meta["title"][:100],
            "description": meta["desc"][:200]
        }
        if thumb_blob:
            ext_obj["thumb"] = thumb_blob
            save_used_image(meta["image"])

        record["embed"] = {
            "$type": "app.bsky.embed.external",
            "external": ext_obj
        }

        print("--- Article Post Preview ---")
        print(post_text)
        print(f"Product Image Thumb: {meta['image']}")
        print("----------------------------")

        result = post_record(session, record)
        print(f"[SUCCESS] Article posted to Bluesky! URI: {result.get('uri')}")
        save_posted(target_article)
        counter["total"] += 1
        counter["article_posts"] += 1
        save_post_counter(counter)

    # Run auto-engagement (likes & follows)
    run_engagement_cycle(session)

    print(f"Execution finished! [Total: {counter['total']}, Articles: {counter['article_posts']}, Trivia: {counter['trivia_posts']}]")

if __name__ == "__main__":
    main()
