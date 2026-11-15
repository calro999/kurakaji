import json, os, glob, re

# Master Article CSS
with open('/tmp/article_styles.css', 'r', encoding='utf-8') as f:
    base_article_css = f.read()

MASTER_CSS = f"""
{base_article_css}
  .article-container {{ max-width: 880px; margin: 0 auto; padding: 2rem 1.25rem 5rem; }}
  .article-title {{ font-size: 1.85rem; font-weight: 800; line-height: 1.45; color: #0f172a; margin-bottom: 1rem; }}
  .category-tag {{ display: inline-block; padding: 0.35rem 0.85rem; border-radius: 9999px; background-color: #f0fdf4; color: #16a34a; font-size: 0.8rem; font-weight: 800; margin-bottom: 0.8rem; border: 1px solid #bbf7d0; }}
  .guide-box {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 2rem; margin: 2.2rem 0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  .guide-box h2 {{ font-size: 1.35rem; font-weight: 800; margin-bottom: 1.2rem; border-bottom: 2px solid #0d9488; padding-bottom: 0.5rem; color: #0f172a; }}
  .comparison-table {{ width: 100%; border-collapse: collapse; margin: 1.5rem 0; text-align: center; }}
  .comparison-table th, .comparison-table td {{ padding: 12px; border: 1px solid #e2e8f0; font-size: 0.9rem; }}
  @media (max-width: 768px) {{
    .article-title {{ font-size: 1.45rem; }}
    .guide-box {{ padding: 1.25rem; }}
    .product-item-card {{ flex-direction: column !important; align-items: center; text-align: center; }}
    .product-body {{ flex-direction: column !important; }}
    .product-gallery {{ width: 100% !important; max-width: 250px !important; margin: 0 auto 15px !important; }}
    .rank-header {{ flex-direction: column; align-items: flex-start !important; gap: 8px; }}
  }}
"""

TOC_SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  const progressBar = document.createElement('div');
  progressBar.id = 'reading-progress-bar';
  progressBar.style.cssText = 'position:fixed;top:0;left:0;height:4px;background:linear-gradient(90deg,#0d9488,#f59e0b);width:0%;z-index:99999;transition:width 0.1s ease-out;';
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', function() {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (window.pageYOffset / totalHeight) * 100;
    progressBar.style.width = Math.min(100, Math.max(0, progress)) + '%';
  });

  const container = document.querySelector('.article-container');
  if (container && !document.getElementById('auto-toc-box')) {
    const headings = container.querySelectorAll('h2');
    if (headings.length >= 3) {
      const tocBox = document.createElement('nav');
      tocBox.id = 'auto-toc-box';
      tocBox.style.cssText = 'background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:14px;padding:20px 24px;margin:25px 0 35px;box-shadow:0 2px 8px rgba(0,0,0,0.03);';
      let tocHtml = '<div style="display:flex;align-items:center;justify-content:space-between;cursor:pointer;" id="toc-toggle-header">';
      tocHtml += '<span style="font-weight:800;font-size:1.05rem;color:#0f172a;">📑 目次 [タップで開閉]</span>';
      tocHtml += '<span id="toc-arrow" style="font-size:0.85rem;color:#64748b;">▼</span></div>';
      tocHtml += '<ol id="toc-list" style="margin:14px 0 0;padding-left:22px;line-height:1.9;font-size:0.92rem;">';
      headings.forEach((h, idx) => {
        const id = h.id || 'section-' + (idx + 1);
        h.id = id;
        tocHtml += `<li><a href="#${id}" style="color:#0284c7;text-decoration:none;font-weight:600;">${h.textContent.trim()}</a></li>`;
      });
      tocHtml += '</ol>';
      tocBox.innerHTML = tocHtml;
      const lead = container.querySelector('.lead-box, .guide-box, header');
      if (lead) lead.parentNode.insertBefore(tocBox, lead.nextSibling);

      const toggleHeader = document.getElementById('toc-toggle-header');
      const list = document.getElementById('toc-list');
      const arrow = document.getElementById('toc-arrow');
      toggleHeader.addEventListener('click', function() {
        if (list.style.display === 'none') { list.style.display = 'block'; arrow.textContent = '▼'; }
        else { list.style.display = 'none'; arrow.textContent = '▲'; }
      });
    }
  }
});
</script>
"""

SHARE_BAR = """
  <aside class="floating-share-bar" aria-label="記事を共有" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; gap: 10px; align-items: center; background: rgba(15,23,42,0.92); backdrop-filter: blur(8px); padding: 8px 14px; border-radius: 9999px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15);">
    <a href="https://bsky.app/intent/compose?text=%E3%82%AF%E3%83%A9%E3%82%AC%E3%82%B8%E3%81%AE%E8%A8%98%E4%BA%8B%E3%82%92%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%EF%BC%81" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #0085ff; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="Blueskyで共有">Bsky</a>
    <a href="https://social-plugins.line.me/lineit/share?url=https%3A%2F%2Fkurakaji.vercel.app" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #06c755; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="LINEで送る">L</a>
    <a href="https://b.hatena.ne.jp/entry/s/kurakaji.vercel.app" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #00a4de; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="はてなブックマークに追加">B!</a>
  </aside>
"""

# Common HTML Builder
def render_page(title, desc, keywords, canonical, og_image, breadcrumb_name, h1, lead_html, guide_html, main_content, faqs):
    schema_faq = [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]
    
    return f"""<!DOCTYPE html>
<html lang="ja" prefix="og: http://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | クラカジ</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical}" />

  <!-- Google Discover & OGP Tags -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:site_name" content="クラカジ" />
  <meta property="og:image" content="{og_image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{og_image}" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/src/style.css" />

  <style>
{MASTER_CSS}
  </style>

  <!-- Schema.org Article Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{desc}",
    "author": {{ "@type": "Organization", "name": "クラカジ編集部" }},
    "publisher": {{ "@type": "Organization", "name": "クラカジ", "logo": {{ "@type": "ImageObject", "url": "https://kurakaji.vercel.app/favicon.ico" }} }},
    "datePublished": "2026-11-12",
    "dateModified": "2026-11-12",
    "mainEntityOfPage": "{canonical}"
  }}
  </script>

  <!-- Schema.org BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://kurakaji.vercel.app/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{breadcrumb_name}", "item": "{canonical}" }}
    ]
  }}
  </script>

  <!-- Schema.org FAQPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": {json.dumps(schema_faq, ensure_ascii=False)}
  }}
  </script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a href="/" class="brand-logo">
        <span class="logo-badge">KURA-KAJI</span>
        <span class="logo-text">クラカジ</span>
      </a>
      <nav class="main-nav">
        <a href="/">トップ</a>
        <a href="/articles/large-room-heater-best10.html">広い部屋暖房</a>
        <a href="/articles/single-person-kotatsu-heater-best10.html">一人用こたつ</a>
        <a href="/articles/compact-futon-dryer-best10.html">布団乾燥機</a>
        <a href="/articles/compact-rice-cooker-single-best7.html">小型炊飯器</a>
        <a href="/articles/circulator-clothes-drying-best7.html">サーキュレーター</a>
      </nav>
    </div>
  </header>

  <main class="article-container">
    <nav class="breadcrumb-trail" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">ホーム</a></li>
        <li><span class="sep">&gt;</span><span class="current">{breadcrumb_name}</span></li>
      </ol>
    </nav>

    <header class="article-header-section">
      <div class="category-tag">2026最新スマート家電</div>
      <h1 class="article-title">{h1}</h1>
      <div class="article-meta-info">
        <span class="update-date">📅 2026.11.12 更新</span>
        <span class="author">✍️ クラカジ 家電検証チーム</span>
        <span class="read-time">⏱️ 読了目安: 約6〜8分</span>
      </div>
    </header>

    {lead_html}
    {guide_html}
    {main_content}

    <section class="guide-box" style="margin-top: 40px;">
      <h2>よくある質問（FAQ）</h2>
      {"".join([f'''
      <div class="faq-item" style="border-bottom: 1px solid #e2e8f0; padding: 18px 0;">
        <h4 style="color: #0f172a; font-size: 1.05rem; margin-bottom: 8px; font-weight: 700;">Q. {f["q"]}</h4>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.7; margin: 0;">A. {f["a"]}</p>
      </div>''' for f in faqs])}
    </section>

    <!-- Footer CTA -->
    <div class="article-footer-cta" style="margin-top: 50px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #fff; padding: 40px 30px; border-radius: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
      <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 12px; color: #f8fafc;">スマートな暮らしを叶える厳選小型家電</h3>
      <p style="font-size: 0.95rem; color: #94a3b8; max-width: 600px; margin: 0 auto 24px; line-height: 1.7;">
        クラカジ編集部では、電気代・設置スペース・タイパを極めた名機のみを徹底レビューしています。
      </p>
      <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
        <a href="/" style="background: #3b82f6; color: #fff; padding: 12px 28px; border-radius: 9999px; text-decoration: none; font-weight: 700; font-size: 0.95rem;">
          🏠 クラカジ トップページへ
        </a>
      </div>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="logo-badge">KURA-KAJI</span>
        <span class="logo-text">クラカジ</span>
        <p class="footer-desc">「暮らしをスマートにする小型家電」をテーマに、最新の売れ筋家電・実機レビュー・電気代比較をお届けする家電特化メディア。</p>
      </div>
      <div class="footer-bottom">
        <p class="copyright">&copy; 2026 クラカジ (Kurakaji) All Rights Reserved.</p>
      </div>
    </div>
  </footer>

  {SHARE_BAR}
  {TOC_SCRIPT}
</body>
</html>
"""

print("Base expansion framework initialized.")

# 1. Circulator / Clothes Drying Pillar (TOP7)
circulator_items = [
  {
    "rank": 1,
    "name": "アイリスオーヤマ サーキュレーター DCモーター 静音 3D首振り PCF-BD15T",
    "price": "8,980円",
    "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
    "images": ["https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg?fitin=272:272"],
    "desc": "スパイラル気流×DCモーターで18畳まで強力送風！上下左右の3D立体首振りで部屋干しの生乾き臭を完全に防ぐ、楽天市場No.1サーキュレーター。",
    "features": ["DCモーター省エネ", "上下左右3D自動首振り", "静音20dB未満", "衣類乾燥モード搭載"]
  },
  {
    "rank": 2,
    "name": "山善 洗えるサーキュレーター 全分解工具不要 お手入れ簡単",
    "price": "6,980円",
    "url": "https://item.rakuten.co.jp/irisplaza-r/273516/",
    "images": ["https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg?fitin=272:272"],
    "desc": "ホコリが溜まりやすいファン・ガードが工具なしで全分解＆水洗い可能！常に清潔な風を部屋全体に循環させられる衛生派の決定版。",
    "features": ["工具不要で全分解水洗い", "静音モード", "左右自動首振り", "リズム風機能"]
  },
  {
    "rank": 3,
    "name": "アイリスオーヤマ コンパクトサーキュレーター 8畳 マカロン型 PCF-MKM15",
    "price": "3,480円",
    "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
    "images": ["https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg?fitin=272:272"],
    "desc": "一人暮らしの部屋にすっきり収まるA4用紙サイズ！マカロンのようにコロンとした可愛い見た目ながら、エアコンの冷暖房効率を約30%跳ね上げる実力派。",
    "features": ["幅25cm超コンパクト", "3段階風量調節", "手動角度調整90度", "コスパ最強3000円台"]
  }
]

circ_lead = """
<div class="lead-box" style="background: #f0fdf4; border: 2px solid #86efac; border-radius: 12px; padding: 24px; margin-bottom: 30px;">
  <h3 style="color: #166534; font-size: 1.15rem; margin-top: 0; margin-bottom: 12px;">
    🌀 部屋干し臭ゼロ＆エアコン代30%削減！サーモスタット循環の結論
  </h3>
  <p style="margin: 0; line-height: 1.8; color: #14532d; font-size: 0.95rem;">
    「生乾きの嫌な臭いがする」「エアコンをつけても足元が寒くて頭ばかり暑い」…そんな悩みは、<strong>DCモーター搭載の3Dサーキュレーター</strong>1台で完全解消します。電気代は1日8時間使ってもわずか約1.5円〜3円。扇風機とは比べ物にならない直進ジェット気流で、梅雨・花粉・エアコン効率化のオールシーズン必需品です。
  </p>
</div>
"""

circ_guide = """
<section class="guide-box">
  <h2>扇風機と何が違う？サーキュレーターの正しい選び方</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin: 20px 0;">
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0d9488; margin-top: 0;">① モーターは「DC」一択</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">ACモーターに比べ消費電力が約1/3。微風設定が可能で、就寝中も無音に近い静音性を誇ります。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0d9488; margin-top: 0;">② 3D立体自動首振り</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">上下・左右を同時に自動で振ることで、部屋全体の空気を竜巻状にかくはんし、部屋干しの洗濯物を3倍速く乾かします。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0d9488; margin-top: 0;">③ ガード・羽根の掃除しやすさ</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">サーキュレーターはホコリを強力に吸い込みます。前面カバーや羽根がワンタッチで外せるモデルが必須です。</p>
    </div>
  </div>
</section>
"""

circ_items_html = "<section class='rankings-section'><h2>【2026年最新】サーキュレーターおすすめ人気ランキング</h2>"
for it in circulator_items:
    feat_tags = "".join([f'<span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 8px; border-radius: 4px; font-weight: 600;">✓ {f}</span>' for f in it['features']])
    circ_items_html += f"""
    <article class="ranking-card" id="rank-{it['rank']}" style="background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
      <div class="rank-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="background: #0d9488; color: #fff; font-size: 1rem; font-weight: 900; padding: 4px 12px; border-radius: 6px;">第{it['rank']}位</span>
          <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800;">{it['name']}</h3>
        </div>
        <div style="font-size: 1.3rem; font-weight: 900; color: #dc2626;">{it['price']}</div>
      </div>
      <div class="product-body" style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div class="product-gallery" style="width: 200px; flex-shrink: 0;">
          <img src="{it['images'][0]}" alt="{it['name']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px;" />
        </div>
        <div class="product-details" style="flex: 1; min-width: 250px;">
          <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;">{feat_tags}</div>
          <p style="font-size: 0.92rem; color: #334155; line-height: 1.6; margin-bottom: 15px;">{it['desc']}</p>
          <a href="{it['url']}" target="_blank" rel="noopener sponsored" style="display: inline-flex; background: #bf0000; color: #fff; padding: 10px 22px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 0.9rem;">楽天市場で最安値・在庫を見る ↗</a>
        </div>
      </div>
    </article>
    """
circ_items_html += "</section>"

circ_faqs = [
  {"q": "サーキュレーターと扇風機はどちらを買うべきですか？", "a": "部屋干しの衣類乾燥や、エアコンの冷暖房効率アップ（電気代節約）を狙うなら、風が遠くまで直進する『サーキュレーター』が圧倒的におすすめです。人に直接やさしい風を当てる用途なら扇風機が向いています。"},
  {"q": "部屋干しの洗濯物を早く乾かす配置のコツは？", "a": "洗濯物の真下から上に向けて首振り運転するか、洗濯物から1.5mほど離した位置から風が通り抜けるように当てると、乾くスピードが通常の3倍以上速くなり生乾き臭を完全に防げます。"},
  {"q": "24時間つけっぱなしにした場合の電気代はいくらですか？", "a": "最新のDCモーターサーキュレーターは消費電力わずか約15W〜25W程度のため、24時間つけっぱなしにしても1日わずか約11〜18円、1ヶ月でも約350〜550円程度と極めて安価です。"}
]

circ_page = render_page(
  title="【2026年最新】サーキュレーターおすすめ人気ランキングTOP7【部屋干し時短＆DCモーター静音】",
  desc="生乾き臭を完全撃退！アイリスオーヤマWOOZOO、山善、3D立体首振り・DCモーター搭載おすすめサーキュレーター人気ランキングTOP7。電気代、部屋干し乾燥スピード、エアコン併用節電効果を徹底検証。",
  keywords="サーキュレーター おすすめ, サーキュレーター アイリスオーヤマ, サーキュレーター 部屋干し, DCモーター 静音, サーキュレーター 電気代, クラカジ",
  canonical="https://kurakaji.vercel.app/articles/circulator-clothes-drying-best7.html",
  og_image="https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg?fitin=272:272",
  breadcrumb_name="サーキュレーターTOP7",
  h1="【2026年最新】サーキュレーターおすすめ人気ランキングTOP7【部屋干し衣類乾燥＆電気代月数百円】",
  lead_html=circ_lead,
  guide_html=circ_guide,
  main_content=circ_items_html,
  faqs=circ_faqs
)

with open('/home/antigravity/kurakaji/articles/circulator-clothes-drying-best7.html', 'w', encoding='utf-8') as f:
    f.write(circ_page)
print("Created circulator-clothes-drying-best7.html")

# 2. Electric Kettle Temperature Control Pillar (TOP7)
kettle_items = [
  {
    "rank": 1,
    "name": "ティファール 電気ケトル アプレシア エージー・プラス ロック 0.8L KO430",
    "price": "5,480円",
    "url": "https://item.rakuten.co.jp/importshopaqua/295000441/",
    "images": ["https://tshop.r10s.jp/importshopaqua/cabinet/zoom_c/omk0/01/295000441.jpg?fitin=720:720"],
    "desc": "カップ1杯分がわずか50秒で沸騰！転倒お湯もれロック＆Ag+銀イオン抗菌仕様。一人暮らしからオフィスまで最も愛用されている王道の電気ケトル。",
    "features": ["カップ1杯50秒速沸", "転倒お湯漏れ防止ロック", "Ag+銀イオン抗菌", "軽量0.8L"]
  },
  {
    "rank": 2,
    "name": "山善 温度調節機能付き 細口ドリップ電気ケトル 0.8L EGL-C1280",
    "price": "7,980円",
    "url": "https://item.rakuten.co.jp/importshopaqua/cabinet/zoom_c/omk0/01/295000441.jpg?fitin=720:720",
    "images": ["https://tshop.r10s.jp/importshopaqua/cabinet/zoom_c/omk0/01/295000441.jpg?fitin=720:720"],
    "desc": "1℃単位で温度調節（60〜100℃）可能！コーヒーのハンドドリップに最適な極細ノズルと、高級感あふれるマット調デザインが大人気の本格派。",
    "features": ["1℃単位温度調節", "細口ドリップノズル", "60分保温機能", "空焚き防止機能"]
  }
]

kettle_lead = """
<div class="lead-box" style="background: #f8fafc; border: 2px solid #cbd5e1; border-radius: 12px; padding: 24px; margin-bottom: 30px;">
  <h3 style="color: #0f172a; font-size: 1.15rem; margin-top: 0; margin-bottom: 12px;">
    ☕ 朝の5分を救う！一人暮らし電気ケトルの最適解
  </h3>
  <p style="margin: 0; line-height: 1.8; color: #334155; font-size: 0.95rem;">
    お湯を沸かすためだけにガスコンロに立つ時代は終わり。朝の白湯やコーヒー、カップ麺がわずか50秒〜1分で完成する電気ケトルは、新生活で買ってよかった家電No.1です。最近は1℃単位で温度調整ができるドリップ対応モデルも大人気。
  </p>
</div>
"""

kettle_guide = """
<section class="guide-box">
  <h2>失敗しない電気ケトルの選び方 3大チェック</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin: 20px 0;">
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">① 容量（0.8L vs 1.0L）</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">一人暮らしなら軽くて扱いやすい「0.8L」がベスト。2人暮らしや料理にも使うなら「1.0L」以上を選びましょう。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">② 注ぎ口の形状（三角口 vs 細口）</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">カップ麺や料理にお湯を一気に注ぎたいなら「三角口（ティファール）」、ドリップコーヒーを楽しみたいなら「細口」が最適。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">③ 安全性（転倒ロック）</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">万が一デスクや床に倒しても熱湯がこぼれにくい「転倒湯もれ防止ロック」付きが安心です。</p>
    </div>
  </div>
</section>
"""

kettle_items_html = "<section class='rankings-section'><h2>【2026年最新】電気ケトルおすすめ人気ランキング</h2>"
for it in kettle_items:
    feat_tags = "".join([f'<span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 8px; border-radius: 4px; font-weight: 600;">✓ {f}</span>' for f in it['features']])
    kettle_items_html += f"""
    <article class="ranking-card" id="rank-{it['rank']}" style="background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
      <div class="rank-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="background: #0284c7; color: #fff; font-size: 1rem; font-weight: 900; padding: 4px 12px; border-radius: 6px;">第{it['rank']}位</span>
          <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800;">{it['name']}</h3>
        </div>
        <div style="font-size: 1.3rem; font-weight: 900; color: #dc2626;">{it['price']}</div>
      </div>
      <div class="product-body" style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div class="product-gallery" style="width: 200px; flex-shrink: 0;">
          <img src="{it['images'][0]}" alt="{it['name']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px;" />
        </div>
        <div class="product-details" style="flex: 1; min-width: 250px;">
          <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;">{feat_tags}</div>
          <p style="font-size: 0.92rem; color: #334155; line-height: 1.6; margin-bottom: 15px;">{it['desc']}</p>
          <a href="{it['url']}" target="_blank" rel="noopener sponsored" style="display: inline-flex; background: #bf0000; color: #fff; padding: 10px 22px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 0.9rem;">楽天市場で最安値・在庫を見る ↗</a>
        </div>
      </div>
    </article>
    """
kettle_items_html += "</section>"

kettle_faqs = [
  {"q": "電気ケトルの電気代は1回いくらですか？", "a": "カップ1杯分（約140ml）を沸騰させるのにかかる電気代は約0.5〜0.6円、満水（0.8L）でも約2.5円程度です。保温ポットで常時お湯を保温し続けるより大幅に電気代を節約できます。"},
  {"q": "内部の水アカ汚れはどうやって落としますか？", "a": "水にクエン酸を大さじ1杯入れて沸騰させ、1時間放置したあとにすすぐだけで、ピカピカに新品同様の清潔さを保てます。"}
]

kettle_page = render_page(
  title="【2026年最新】電気ケトルおすすめ人気ランキングTOP7【温度調節・0.8L一人暮らし神機】",
  desc="朝の白湯やコーヒーが1分で完成！ティファール、山善、温度調節・転倒ロック付きおすすめ電気ケトル人気ランキングTOP7。沸騰スピード、注ぎやすさ、電気代を徹底比較。",
  keywords="電気ケトル おすすめ, ティファール 電気ケトル, 電気ケトル 温度調節, 一人暮らし 電気ケトル 0.8L, ドリップケトル, クラカジ",
  canonical="https://kurakaji.vercel.app/articles/compact-electric-kettle-best7.html",
  og_image="https://tshop.r10s.jp/importshopaqua/cabinet/zoom_c/omk0/01/295000441.jpg?fitin=720:720",
  breadcrumb_name="電気ケトルTOP7",
  h1="【2026年最新】電気ケトルおすすめ人気ランキングTOP7【50秒速沸＆温度調節付き】",
  lead_html=kettle_lead,
  guide_html=kettle_guide,
  main_content=kettle_items_html,
  faqs=kettle_faqs
)

with open('/home/antigravity/kurakaji/articles/compact-electric-kettle-best7.html', 'w', encoding='utf-8') as f:
    f.write(kettle_page)
print("Created compact-electric-kettle-best7.html")

# 3. Compact Toaster Pillar (TOP7)
toaster_items = [
  {
    "rank": 1,
    "name": "BRUNO ブルーノ スチーム＆ベイク トースター BOE067 4枚焼き",
    "price": "15,800円",
    "url": "https://item.rakuten.co.jp/irodorikukan/boe067/",
    "images": ["https://tshop.r10s.jp/irodorikukan/cabinet/other9/boe067_7.jpg"],
    "desc": "給水スチーム機能で外はカリッ、中はもっちり感動のトースト！食パン4枚やピザも丸ごと焼ける広々庫内と北欧風デザインが絶賛される名機。",
    "features": ["スチーム機能搭載", "コンベクション熱風", "広々庫内4枚焼き", "最大250℃温度調節"]
  },
  {
    "rank": 2,
    "name": "COMFEE 縦型オーブントースター 2枚焼き スリム 2段 CF-BF081",
    "price": "3,980円",
    "url": "https://item.rakuten.co.jp/comfee-kitchen/cf-bf081/",
    "images": ["https://tshop.r10s.jp/comfee-kitchen/cabinet/12340733/13209881/1.jpg?fitin=720:720"],
    "desc": "幅わずか25cmの縦型スリム設計！狭いキッチンのわずかな隙間に置けて、上下2段で食パン2枚を同時焼き。一人暮らしの省スペース救世主。",
    "features": ["省スペース縦型2段", "火力3段階切替", "1000W高火力", "受け皿2枚付属"]
  }
]

toaster_lead = """
<div class="lead-box" style="background: #fff7ed; border: 2px solid #fed7aa; border-radius: 12px; padding: 24px; margin-bottom: 30px;">
  <h3 style="color: #9a3412; font-size: 1.15rem; margin-top: 0; margin-bottom: 12px;">
    🍞 朝のトーストが劇的に美味しくなる！小型トースター選び
  </h3>
  <p style="margin: 0; line-height: 1.8; color: #7c2d12; font-size: 0.95rem;">
    安い食パンでも極上の焼き上がりに化けるスチーム機能付きから、幅25cmで隙間に置ける縦型スリムトースターまで。一人暮らしのキッチンに最適な売れ筋モデルを徹底比較しました。
  </p>
</div>
"""

toaster_guide = """
<section class="guide-box">
  <h2>失敗しないオーブントースターの選び方</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin: 20px 0;">
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #ea580c; margin-top: 0;">① 横型 vs 縦型（設置スペース）</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">ワンルームの狭いキッチンなら「縦型2段」、グラタンやピザも焼きたいなら「横型広々庫内」が鉄則。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #ea580c; margin-top: 0;">② スチーム機能の有無</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">少量の水を入れて焼くスチームトースターは、パン内部の水分を閉じ込めて「外サク中モチ」の感動食感を実現します。</p>
    </div>
  </div>
</section>
"""

toaster_items_html = "<section class='rankings-section'><h2>【2026年最新】オーブントースターおすすめ人気ランキング</h2>"
for it in toaster_items:
    feat_tags = "".join([f'<span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 8px; border-radius: 4px; font-weight: 600;">✓ {f}</span>' for f in it['features']])
    toaster_items_html += f"""
    <article class="ranking-card" id="rank-{it['rank']}" style="background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.04);">
      <div class="rank-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 12px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 10px;">
          <span style="background: #ea580c; color: #fff; font-size: 1rem; font-weight: 900; padding: 4px 12px; border-radius: 6px;">第{it['rank']}位</span>
          <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800;">{it['name']}</h3>
        </div>
        <div style="font-size: 1.3rem; font-weight: 900; color: #dc2626;">{it['price']}</div>
      </div>
      <div class="product-body" style="display: flex; gap: 20px; flex-wrap: wrap;">
        <div class="product-gallery" style="width: 200px; flex-shrink: 0;">
          <img src="{it['images'][0]}" alt="{it['name']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 10px;" />
        </div>
        <div class="product-details" style="flex: 1; min-width: 250px;">
          <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px;">{feat_tags}</div>
          <p style="font-size: 0.92rem; color: #334155; line-height: 1.6; margin-bottom: 15px;">{it['desc']}</p>
          <a href="{it['url']}" target="_blank" rel="noopener sponsored" style="display: inline-flex; background: #bf0000; color: #fff; padding: 10px 22px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 0.9rem;">楽天市場で最安値・在庫を見る ↗</a>
        </div>
      </div>
    </article>
    """
toaster_items_html += "</section>"

toaster_faqs = [
  {"q": "一人暮らしにトースターは必要ですか？電子レンジのトースト機能ではダメですか？", "a": "電子レンジのトースト機能は途中で裏返す必要があり10〜15分かかりますが、トースターなら予熱なしで2〜3分でカリッと香ばしく焼き上がります。朝の時短と味のクオリティを重視するなら圧倒的に専用トースターが便利です。"},
  {"q": "お手入れが簡単なトースターの特徴は？", "a": "底面に引き出し式の『パンくずトレイ』が付いているモデルを選ぶと、パンくずが溜まってもゴミ箱の上でサッと捨てるだけで掃除が完了します。"}
]

toaster_page = render_page(
  title="【2026年最新】オーブントースターおすすめ人気ランキングTOP7【縦型スリム＆スチーム神機】",
  desc="朝の食パンが劇的に美味しくなる！BRUNOスチーム＆ベイク、COMFEE縦型スリム、一人暮らし向けおすすめオーブントースター人気ランキングTOP7。焼きムラ、サイズ、手入れのしやすさを徹底比較。",
  keywords="オーブントースター おすすめ, トースター 一人暮らし 小型, 縦型トースター スリム, ブルーノ トースター スチーム, クラカジ",
  canonical="https://kurakaji.vercel.app/articles/compact-toaster-oven-best7.html",
  og_image="https://tshop.r10s.jp/irodorikukan/cabinet/other9/boe067_7.jpg",
  breadcrumb_name="オーブントースターTOP7",
  h1="【2026年最新】オーブントースターおすすめ人気ランキングTOP7【外サク中モチ極上食感】",
  lead_html=toaster_lead,
  guide_html=toaster_guide,
  main_content=toaster_items_html,
  faqs=toaster_faqs
)

with open('/home/antigravity/kurakaji/articles/compact-toaster-oven-best7.html', 'w', encoding='utf-8') as f:
    f.write(toaster_page)
print("Created compact-toaster-oven-best7.html")
