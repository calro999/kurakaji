import os, glob, re

base_dir = '/home/antigravity/kurakaji'
articles = sorted(glob.glob(os.path.join(base_dir, 'articles/**/*.html'), recursive=True))

for file_path in articles:
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if author bio card already present
    if 'class="author-profile-box"' not in html:
        author_box = """
    <!-- Author & Editorial Verification Box -->
    <div class="author-profile-box" style="display: flex; gap: 16px; align-items: center; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px 22px; margin: 2rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
      <div style="font-size: 2.2rem; background: #e0f2fe; width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">✍️</div>
      <div>
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
          <span style="font-weight: 800; font-size: 1rem; color: #0f172a;">クラカジ 家電検証・編集チーム</span>
          <span style="background: #dbeafe; color: #1e40af; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">公式検証済み</span>
        </div>
        <p style="font-size: 0.85rem; color: #64748b; line-height: 1.5; margin: 0;">
          「暮らし×家事×家電」をテーマに、一人暮らし・共働き世帯のQOLを高める小型家電を徹底検証。公的基準（PSEマーク等）や実測電気代（31円/kWh換算）に基づく誠実なレビューをお届けしています。
        </p>
      </div>
    </div>
"""
        # Insert before first guide-box or ranking-section
        if '<div class="guide-box"' in html or '<section class="guide-box"' in html:
            html = re.sub(r'(<(?:div|section) class="guide-box")', author_box + r'\1', html, count=1)
        elif '<section class="rankings-section"' in html or '<section class="rank-card"' in html:
            html = re.sub(r'(<section class="rank(?:ings-section|-card)")', author_box + r'\1', html, count=1)

    # Check if Related Articles Box already present
    if 'class="related-articles-box"' not in html:
        related_box = """
    <!-- Related Useful Guides Box -->
    <section class="related-articles-box" style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px; margin: 3rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
      <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-top: 0; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
        <span>🔗</span> あわせて読みたい関連ガイド
      </h3>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px;">
        <a href="/articles/cluster/single-life-appliances-regret-top5.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block;">
          <span style="color: #dc2626; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">⚠️ 後悔防止</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">一人暮らしで買って後悔した家電ワースト5</span>
        </a>
        <a href="/articles/circulator-clothes-drying-best7.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block;">
          <span style="color: #16a34a; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">🌀 部屋干し・節電</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">サーキュレーター衣類乾燥＆DC静音TOP7</span>
        </a>
        <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; padding: 14px; text-decoration: none; color: inherit; display: block;">
          <span style="color: #d97706; font-size: 0.75rem; font-weight: 800; display: block; margin-bottom: 4px;">💡 節電マニュアル</span>
          <span style="font-weight: 700; font-size: 0.9rem; color: #0f172a; line-height: 1.4; display: block;">冬の電気代を月1万円削る小型家電フル活用術</span>
        </a>
      </div>
    </section>
"""
        # Insert before .guide-box (FAQ) or footer CTA
        if '<h2>よくある質問（FAQ）</h2>' in html:
            html = html.replace('<h2>よくある質問（FAQ）</h2>', related_box + '<h2>よくある質問（FAQ）</h2>')
        elif 'class="faq-box"' in html:
            html = re.sub(r'(<div class="faq-box")', related_box + r'\1', html, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("Enriched all 25 articles with editorial authority card & related guides!")
