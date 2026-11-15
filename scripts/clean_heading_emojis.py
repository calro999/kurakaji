import os, glob, re

base_dir = '/home/antigravity/kurakaji'
files = glob.glob(os.path.join(base_dir, 'articles/**/*.html'), recursive=True) + [
    os.path.join(base_dir, 'index.html'),
    os.path.join(base_dir, 'about.html'),
    os.path.join(base_dir, 'terms.html'),
    os.path.join(base_dir, 'privacy.html')
]

# Emoji regex covering common pictographs and variation selectors
EMOJI_PATTERN = re.compile(
    r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\ufe00-\ufe0f]',
    flags=re.UNICODE
)

def clean_tag_text(match):
    tag_open = match.group(1)
    content = match.group(2)
    tag_close = match.group(3)
    # Remove emojis from content
    clean_content = EMOJI_PATTERN.sub('', content)
    # Clean leading/trailing spaces
    clean_content = re.sub(r'^\s+|\s+$', '', clean_content)
    clean_content = re.sub(r'>\s+', '>', clean_content)
    return f"{tag_open}{clean_content}{tag_close}"

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Clean h1, h2, h3, h4, h5, h6
    html = re.sub(r'(<h[1-6][^>]*>)(.*?)(</h[1-6]>)', clean_tag_text, html, flags=re.DOTALL)
    
    # Also clean section badges like "✨ 2026年最新 QOL向上ギア" -> "2026年最新 QOL向上ギア"
    html = html.replace('✨ 2026年最新 QOL向上ギア', '2026年最新 QOL向上ギア')
    html = html.replace('🔥 2026冬の検索流入独占・特別特集', '2026冬の検索流入独占・特別特集')
    html = html.replace('🌟 クラカジ編集部 厳選特集＆検証コラム（全25本）', 'クラカジ編集部 厳選特集＆検証コラム（全25本）')
    html = html.replace('⚡ 10秒でわかる冬の電気代診断', '10秒でわかる冬の電気代診断')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("All headings cleaned of decorative emojis!")
