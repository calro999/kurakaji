import os, glob, re

base_dir = '/home/antigravity/kurakaji'
articles = sorted(glob.glob(os.path.join(base_dir, 'articles/**/*.html'), recursive=True))

RELATED_2X2_HTML = """    <!-- Related Useful Guides Box (2x2 Grid) -->
    <section class="related-articles-box" style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px; margin: 3rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
      <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
        <span>🔗</span> あわせて読みたい厳選ガイド（おすすめ4選）
      </h3>
      <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px;">
        <a href="/articles/cluster/single-life-appliances-regret-top5.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block; transition: border-color 0.2s;">
          <span style="color: #dc2626; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">⚠️ 後悔防止</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">一人暮らしで買って後悔した家電ワースト5</span>
        </a>
        <a href="/articles/circulator-clothes-drying-best7.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block; transition: border-color 0.2s;">
          <span style="color: #16a34a; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">🌀 部屋干し速乾</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">サーキュレーター衣類乾燥＆DC静音TOP7</span>
        </a>
        <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block; transition: border-color 0.2s;">
          <span style="color: #d97706; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">💡 節電マニュアル</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">冬の電気代を月1万円削る小型家電フル活用術</span>
        </a>
        <a href="/articles/handy-garment-steamer-best7.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block; transition: border-color 0.2s;">
          <span style="color: #db2777; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">👔 朝のタイパ</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">一人暮らし用ハンディ衣類スチーマーTOP7</span>
        </a>
      </div>
    </section>"""

for path in articles:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # If related-articles-box already exists, replace it
    if 'class="related-articles-box"' in html:
        html = re.sub(r'<!-- Related Useful Guides Box.*?<\/section>', RELATED_2X2_HTML, html, flags=re.DOTALL)
        html = re.sub(r'<section class="related-articles-box".*?<\/section>', RELATED_2X2_HTML, html, flags=re.DOTALL)
    else:
        # insert before FAQ
        if '<h2>よくある質問（FAQ）</h2>' in html:
            html = html.replace('<h2>よくある質問（FAQ）</h2>', RELATED_2X2_HTML + '\n    <h2>よくある質問（FAQ）</h2>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Updated Related Guides to 4 items in a 2x2 grid across all 25 articles!")
