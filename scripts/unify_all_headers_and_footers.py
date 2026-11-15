import os, glob, re

base_dir = '/home/antigravity/kurakaji'
articles = sorted(glob.glob(os.path.join(base_dir, 'articles/**/*.html'), recursive=True))

MASTER_HEADER = """  <header class="site-header">
    <div class="header-inner">
      <div class="brand-block">
        <div class="brand-icon">⚡</div>
        <div class="brand-text-wrap">
          <a href="/" class="brand-title">クラカジ</a>
          <span class="brand-catchphrase">暮らしをスマートにする小型家電</span>
        </div>
      </div>
      <nav class="header-nav">
        <a href="/" class="nav-link"><span>トップへ戻る</span></a>
        <a href="/#catalog" class="nav-link"><span>カタログ一覧</span></a>
        <a href="/#editorial" class="nav-link"><span>厳選コラム</span></a>
      </nav>
    </div>
  </header>"""

MASTER_FOOTER = """  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand-note">
        <strong style="color: var(--color-text-main); font-size: 1.05rem;">クラカジ</strong>
        <p style="margin-top: 0.4rem; color: var(--color-text-muted);">
          暮らしをスマートにする小型家電・生活雑貨家電のセレクトカタログメディア。<br />
          ※当サイトはアフィリエイト広告を利用して商品をご紹介しています。
        </p>
      </div>

      <nav class="footer-nav" aria-label="フッターリンク">
        <a href="/about.html">クラカジについて・編集部紹介</a>
        <a href="/terms.html">利用規約</a>
        <a href="/privacy.html">プライバシーポリシー</a>
      </nav>

      <div class="copyright">
        &copy; 2026 クラカジ (Kurakaji) All Rights Reserved.
      </div>
    </div>
  </footer>"""

# Process all 25 articles
for file_path in articles:
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace header
    html = re.sub(r'<header class="site-header">.*?</header>', MASTER_HEADER, html, flags=re.DOTALL)
    
    # 2. Replace footer
    html = re.sub(r'<footer class="site-footer">.*?</footer>', MASTER_FOOTER, html, flags=re.DOTALL)

    # 3. Ensure responsive stylesheet link
    if '<link rel="stylesheet" href="/src/style.css"' not in html:
        html = html.replace('</head>', '  <link rel="stylesheet" href="/src/style.css" />\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Standardized header & footer for: {os.path.relpath(file_path, base_dir)}")

# Also update index.html footer
with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
    index_html = f.read()

index_html = re.sub(r'<footer class="site-footer">.*?</footer>', MASTER_FOOTER, index_html, flags=re.DOTALL)
with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_html)
print("Updated index.html footer links!")
