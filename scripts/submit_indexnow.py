"""
full_crawler_ping.py
DuckDuckGo, Bing, Yandex, Naver, Seznam, Google, etc.
全ての検索エンジン・AIクローラーへIndexNow一斉配信＆Sitemap Pingを実行するスクリプト
"""

import os
import json
import urllib.request
import ssl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOAD_FILE = os.path.join(BASE_DIR, "scripts", "indexnow_payload.json")

def ping_crawlers():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[WARN] {PAYLOAD_FILE} not found. Running generator...")
        import generate_llms_and_indexnow
    
    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    urls = payload.get("urlList", [])
    print(f"=== 全クローラー/LLM向け インデックス配信開始: {len(urls)} URLs ===")

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Kurakaji-IndexNow-Client/2.0"
    }

    # IndexNow API エンドポイント
    # DuckDuckGo は Bing/IndexNow のインデックスパートナーであり、IndexNow に送信すると Bing, DuckDuckGo, Yandex, Naver, Seznam に自動共有・クロールされます
    indexnow_endpoints = [
        "https://api.indexnow.org/IndexNow",
        "https://www.bing.com/IndexNow",
        "https://yandex.com/indexnow",
        "https://searchadvisor.naver.com/indexnow",
        "https://search.seznam.cz/indexnow"
    ]

    print("\n--- [1] IndexNow API エンドポイント一斉送信 (DuckDuckGo, Bing, Yandex, Naver等) ---")
    for ep in indexnow_endpoints:
        try:
            req = urllib.request.Request(ep, data=data, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as res:
                print(f"[SUCCESS] IndexNow -> {ep} (HTTP {res.status})")
        except urllib.error.HTTPError as e:
            if e.code in [200, 202]:
                print(f"[SUCCESS] IndexNow -> {ep} (HTTP {e.code})")
            else:
                print(f"[INFO] IndexNow -> {ep} (HTTP {e.code}: {e.reason})")
        except Exception as e:
            print(f"[WARN] IndexNow -> {ep} Error: {e}")

    # Sitemap Ping (Google, Bing / DuckDuckGo)
    sitemap_url = "https://kurakaji.vercel.app/sitemap.xml"
    sitemap_pings = [
        f"https://www.google.com/ping?sitemap={sitemap_url}",
        f"https://www.bing.com/ping?sitemap={sitemap_url}"
    ]

    print("\n--- [2] 検索エンジン Sitemap Ping (Google, Bing) ---")
    for ping_ep in sitemap_pings:
        try:
            req = urllib.request.Request(ping_ep, headers={"User-Agent": "Mozilla/5.0 (compatible; KurakajiBot/2.0)"})
            with urllib.request.urlopen(req, context=ctx, timeout=15) as res:
                print(f"[SUCCESS] Sitemap Ping -> {ping_ep} (HTTP {res.status})")
        except urllib.error.HTTPError as e:
            print(f"[INFO] Sitemap Ping -> {ping_ep} (HTTP {e.code})")
        except Exception as e:
            print(f"[WARN] Sitemap Ping -> {ping_ep} Error: {e}")

    print("\n全インデックス配信が完了しました！")

if __name__ == "__main__":
    ping_crawlers()
