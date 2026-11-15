"""
submit_indexnow.py
IndexNow APIへ即時送信するスクリプト（Bing, Yandex, Naver 等の検索エンジンに全URLを即時通知）
"""

import os
import json
import urllib.request
import ssl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOAD_FILE = os.path.join(BASE_DIR, "scripts", "indexnow_payload.json")

def submit_to_indexnow():
    if not os.path.exists(PAYLOAD_FILE):
        print(f"[WARN] {PAYLOAD_FILE} not found. Running generator...")
        import generate_llms_and_indexnow
    
    with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # IndexNow API エンドポイント（Bing / API）
    endpoints = [
        "https://api.indexnow.org/IndexNow",
        "https://www.bing.com/IndexNow"
    ]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Kurakaji-IndexNow-Client/1.0"
    }

    print(f"=== IndexNow 送信開始: {len(payload.get('urlList', []))} 件のURL ===")
    for ep in endpoints:
        try:
            req = urllib.request.Request(ep, data=data, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as res:
                print(f"[SUCCESS] IndexNow submitted to {ep} (HTTP {res.status})")
        except urllib.error.HTTPError as e:
            # 200 or 202 is success. Some return 202 Accepted
            if e.code in [200, 202]:
                print(f"[SUCCESS] IndexNow accepted by {ep} (HTTP {e.code})")
            else:
                print(f"[INFO] IndexNow {ep} returned: {e.code} {e.reason}")
        except Exception as e:
            print(f"[WARN] IndexNow error with {ep}: {e}")

if __name__ == "__main__":
    submit_to_indexnow()
