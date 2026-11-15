import re, glob, os

BASE_DIR = '/home/antigravity/kurakaji'

with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<section id="editorial"')
if start_idx == -1:
    print("editorial not found!")
    exit(1)

end_idx = html.find('</section>', start_idx) + len('</section>')

# Collect all articles
pillar_articles = sorted(glob.glob(os.path.join(BASE_DIR, 'articles/*.html')))
cluster_articles = sorted(glob.glob(os.path.join(BASE_DIR, 'articles/cluster/*.html')))

def build_card(filepath, is_pillar=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title_m = re.search(r'<title>(.*?)</title>', content)
    title = title_m.group(1).replace(' | クラカジ', '') if title_m else ''
    
    desc_m = re.search(r'<meta name="description" content="(.*?)"', content)
    desc = desc_m.group(1) if desc_m else ''
    
    tag_m = re.search(r'<span class="article-tag">(.*?)</span>', content)
    tag = tag_m.group(1) if tag_m else ('人気ランキング' if is_pillar else '解説コラム')
    
    rel_path = os.path.relpath(filepath, BASE_DIR)
    
    border_color = "#38bdf8" if is_pillar else "#cbd5e1"
    bg_tag = "#f0f9ff" if is_pillar else "#f8fafc"
    text_tag = "#0284c7" if is_pillar else "#64748b"
    btn_text = "ランキングを読む →" if is_pillar else "解説記事を読む →"
    
    return f"""
        <article style="background: #fff; padding: 1.35rem; border-radius: var(--radius-lg); border: 1.5px solid {border_color}; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: {bg_tag}; font-size: 0.75rem; font-weight: 800; color: {text_tag};">{tag}</span>
            <span style="font-size: 0.75rem; color: var(--color-text-muted);">{'TOP7〜10' if is_pillar else '検証コラム'}</span>
          </div>
          <h3 style="font-size: 1rem; font-weight: 800; margin-bottom: 0.65rem; line-height: 1.45;">
            <a href="/{rel_path}" style="color: var(--color-text-main); text-decoration: none;">{title}</a>
          </h3>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.1rem; flex: 1;">
            {desc[:75]}…
          </p>
          <a href="/{rel_path}" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.6rem 1rem; background: {'#0284c7' if is_pillar else '#f1f5f9'}; color: {'#fff' if is_pillar else '#0284c7'}; font-weight: 700; font-size: 0.85rem; border-radius: var(--radius-md); text-decoration: none;">
            {btn_text}
          </a>
        </article>"""

pillar_cards_html = "".join([build_card(f, True) for f in pillar_articles])
cluster_cards_html = "".join([build_card(f, False) for f in cluster_articles])

new_editorial_section = f"""<section id="editorial" style="margin-top: 4.5rem; padding-top: 3rem; border-top: 1px solid var(--color-border);">
      <div style="text-align: center; margin-bottom: 2.25rem;">
        <span style="font-size: 0.8rem; font-weight: 800; color: #0284c7; letter-spacing: 0.05em; text-transform: uppercase; background: #e0f2fe; padding: 0.25rem 0.8rem; border-radius: var(--radius-full);">クラカジ編集部 厳選特集＆検証コラム（全50本）</span>
        <h2 style="font-size: 1.65rem; font-weight: 800; color: var(--color-text-main); margin-top: 0.6rem;">暮らしを激変させる厳選小型家電ガイド</h2>
        <p style="color: var(--color-text-muted); font-size: 0.95rem; margin-top: 0.4rem;">一人暮らし・狭い部屋・冬籠り防寒・電気代節約・タイパを極めた全50本の名機徹底検証。</p>
      </div>

      <!-- Pillar Rankings Grid (27 Pillar Guides) -->
      <h3 style="font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem;">
        人気小型家電おすすめランキングTOP7〜10（全{len(pillar_articles)}本）
      </h3>
      <div class="editorial-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3.5rem;">
        {pillar_cards_html}
      </div>

      <!-- Cluster Columns Grid (23 Cluster Columns) -->
      <h3 style="font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem;">
        家電の選び方・電気代比較・失敗回避コラム（全{len(cluster_articles)}本）
      </h3>
      <div class="editorial-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        {cluster_cards_html}
      </div>
    </section>"""

new_html = html[:start_idx] + new_editorial_section + html[end_idx:]

with open(os.path.join(BASE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"index.html successfully rebuilt with all {len(pillar_articles) + len(cluster_articles)} articles!")
