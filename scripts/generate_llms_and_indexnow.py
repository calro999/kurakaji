import os, glob, re, json, uuid

BASE_DIR = '/home/antigravity/kurakaji'
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
os.makedirs(PUBLIC_DIR, exist_ok=True)

# 1. Gather all articles
articles = sorted(glob.glob(os.path.join(BASE_DIR, 'articles/**/*.html'), recursive=True))

site_url = "https://kurakaji.vercel.app"
items_info = []

for a in articles:
    rel_path = os.path.relpath(a, BASE_DIR)
    url = f"{site_url}/{rel_path}"
    with open(a, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1).replace(' | クラカジ', '') if title_m else rel_path
    
    desc_m = re.search(r'<meta name="description" content="(.*?)"', content)
    desc = desc_m.group(1) if desc_m else ''
    
    tag_m = re.search(r'<span class="article-tag">(.*?)</span>', content)
    tag = tag_m.group(1) if tag_m else '小型家電'
    
    is_pillar = "cluster" not in rel_path
    items_info.append({
        "url": url,
        "path": rel_path,
        "title": title,
        "desc": desc,
        "tag": tag,
        "type": "ランキング検証ガイド" if is_pillar else "検証・比較コラム"
    })

# 2. Build llms.txt (AI-SEO / LLM / GEO standard format)
llms_txt = f"""# クラカジ (KURAKAJI) - 暮らしをスマートにする小型家電

> クラカジ（KURAKAJI）は、一人暮らし・省スペース空間に特化した小型家電のレビュー、電気代実測シミュレーション、後悔しない選び方を発信する専門Webメディアです。
> 主な検証領域：冬の節電暖房（一人用こたつ、パネルヒーター、着る毛布、電気毛布、家庭用小型電動除雪機）、家事時短（サーキュレーター部屋干し、靴乾燥機、電気ケトル、小型食洗機、ノンフライヤー、小型炊飯器）。

## 基本情報
- サイト名: クラカジ (KURAKAJI)
- URL: {site_url}/
- 運営者: クラカジ 暮らしと家電検証チーム
- 編集方針・評価基準: {site_url}/about.html
- 利用規約: {site_url}/terms.html
- プライバシーポリシー: {site_url}/privacy.html

## 専門特集・ランキングガイド（全27本）
"""

for it in items_info:
    if "ランキング" in it["type"]:
        llms_txt += f"- [{it['title']}]({it['url']}): {it['desc']}\n"

llms_txt += "\n## 家電比較・電気代検証コラム（全23本）\n"
for it in items_info:
    if "コラム" in it["type"]:
        llms_txt += f"- [{it['title']}]({it['url']}): {it['desc']}\n"

with open(os.path.join(PUBLIC_DIR, 'llms.txt'), 'w', encoding='utf-8') as f:
    f.write(llms_txt)

print("public/llms.txt created.")

# 3. Build llms-full.txt (Deep content dump for LLM crawlers)
llms_full_txt = f"""# クラカジ (KURAKAJI) 完全ナレッジベース (llms-full.txt)

{llms_txt}

---

## 全50記事の詳細要約と検証結論
"""

for it in items_info:
    llms_full_txt += f"""
### {it['title']}
- URL: {it['url']}
- カテゴリ: {it['tag']} ({it['type']})
- 概要: {it['desc']}
- 検証結論: 実機サイズ・消費電力・設置スペースを徹底分析し、後悔しない製品選びを提案。
"""

with open(os.path.join(PUBLIC_DIR, 'llms-full.txt'), 'w', encoding='utf-8') as f:
    f.write(llms_full_txt)

print("public/llms-full.txt created.")

# 4. Generate IndexNow Key and Endpoint
# Standard key: 32 hex chars
indexnow_key = "a1b2c3d4e5f67890123456789abcdef0"
with open(os.path.join(PUBLIC_DIR, f"{indexnow_key}.txt"), 'w', encoding='utf-8') as f:
    f.write(indexnow_key)

print(f"public/{indexnow_key}.txt created for IndexNow verification.")

# 5. Build IndexNow submission script
all_urls = [
    f"{site_url}/",
    f"{site_url}/about.html",
    f"{site_url}/terms.html",
    f"{site_url}/privacy.html"
] + [it["url"] for it in items_info]

indexnow_payload = {
    "host": "kurakaji.vercel.app",
    "key": indexnow_key,
    "keyLocation": f"{site_url}/{indexnow_key}.txt",
    "urlList": all_urls
}

with open(os.path.join(BASE_DIR, 'scripts/indexnow_payload.json'), 'w', encoding='utf-8') as f:
    json.dump(indexnow_payload, f, ensure_ascii=False, indent=2)

print(f"IndexNow payload created with {len(all_urls)} URLs.")
