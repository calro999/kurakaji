import os, glob, re, json

base_dir = '/home/antigravity/kurakaji'
articles = sorted(glob.glob(os.path.join(base_dir, 'articles/**/*.html'), recursive=True))

ORGANIZATION_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": "https://kurakaji.vercel.app/#organization",
    "name": "クラカジ",
    "alternateName": ["Kurakaji", "クラカジ編集部"],
    "url": "https://kurakaji.vercel.app/",
    "logo": {
        "@type": "ImageObject",
        "@id": "https://kurakaji.vercel.app/#logo",
        "url": "https://kurakaji.vercel.app/favicon.svg",
        "caption": "クラカジ ロゴ"
    },
    "description": "暮らしをスマートにする小型家電・生活雑貨家電のセレクト比較メディア。一人暮らしや狭い部屋にフィットする省スペース・省エネ家電を検証。",
    "sameAs": [
        "https://bsky.app/profile/kurakaden.bsky.social"
    ],
    "publishingPrinciples": "https://kurakaji.vercel.app/about.html"
}

WEBSITE_SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": "https://kurakaji.vercel.app/#website",
    "url": "https://kurakaji.vercel.app/",
    "name": "クラカジ",
    "description": "暮らしをスマートにする小型家電・生活家電専門カタログメディア",
    "publisher": {
        "@id": "https://kurakaji.vercel.app/#organization"
    },
    "inLanguage": "ja"
}

# Update index.html
with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
    index_html = f.read()

# Add favicon links to index.html if missing
favicon_tags = """  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="icon" type="image/x-icon" href="/favicon.ico" />
  <link rel="apple-touch-icon" href="/favicon.svg" />"""

if '/favicon.svg' not in index_html:
    index_html = index_html.replace('</head>', f"{favicon_tags}\n</head>")

# Inject structured data to index.html
index_schema_script = f"""  <script type="application/ld+json">
{json.dumps(ORGANIZATION_SCHEMA, ensure_ascii=False, indent=2)}
  </script>
  <script type="application/ld+json">
{json.dumps(WEBSITE_SCHEMA, ensure_ascii=False, indent=2)}
  </script>"""

if 'id="organization"' not in index_html and '#organization' not in index_html:
    index_html = index_html.replace('</head>', f"{index_schema_script}\n</head>")

with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Updated index.html with Organization and WebSite Schemas!")

# Process all 25 articles
for path in articles:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add favicon links if not present
    if '/favicon.svg' not in html:
        html = html.replace('</head>', f"{favicon_tags}\n</head>")

    # 2. Extract article title and description
    title_m = re.search(r'<title>(.*?) \| クラカジ</title>', html)
    title = title_m.group(1) if title_m else "小型家電ガイド"
    
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    desc = desc_m.group(1) if desc_m else ""

    canonical_m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    canonical = canonical_m.group(1) if canonical_m else f"https://kurakaji.vercel.app/{os.path.relpath(path, base_dir)}"

    og_image_m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    og_image = og_image_m.group(1) if og_image_m else "https://kurakaji.vercel.app/favicon.svg"

    # Construct complete E-E-A-T & AI Engine Optimized Article Schema
    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "@id": f"{canonical}#article",
        "isPartOf": {
            "@type": "WebPage",
            "@id": canonical
        },
        "headline": title,
        "description": desc,
        "image": [og_image],
        "datePublished": "2026-11-12T00:00:00+09:00",
        "dateModified": "2026-11-12T18:00:00+09:00",
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical
        },
        "author": {
            "@type": "Organization",
            "@id": "https://kurakaji.vercel.app/#organization",
            "name": "クラカジ 家電検証・編集チーム",
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
        "inLanguage": "ja",
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [".article-title", ".article-lead", ".guide-box p"]
        }
    }

    # Replace old Article schema
    old_schema_pattern = re.compile(r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org",\s*"@type":\s*"Article".*?<\/script>', re.DOTALL)
    
    new_schema_str = f"""<script type="application/ld+json">
{json.dumps(article_schema, ensure_ascii=False, indent=2)}
  </script>"""

    if old_schema_pattern.search(html):
        html = old_schema_pattern.sub(new_schema_str, html, count=1)
    else:
        html = html.replace('</head>', f"  {new_schema_str}\n</head>")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Injected AI & Crawler optimized E-E-A-T schemas across all 25 articles!")
