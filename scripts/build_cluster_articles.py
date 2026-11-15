import os, json

# Ensure cluster directory exists
os.makedirs('/home/antigravity/kurakaji/articles/cluster', exist_ok=True)

# Common styling and header/footer templates matching Kurakaji design system
def get_header(title, desc, keywords, canonical_url, og_image, breadcrumb_name):
    return f"""<!DOCTYPE html>
<html lang="ja" prefix="og: http://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | クラカジ</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical_url}" />

  <!-- OGP -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title} | クラカジ" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:site_name" content="クラカジ" />
  <meta property="og:image" content="{og_image}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title} | クラカジ" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{og_image}" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/src/style.css" />
"""

def get_footer():
    return """
    <!-- Footer CTA -->
    <div class="article-footer-cta" style="margin-top: 50px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #fff; padding: 40px 30px; border-radius: 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15);">
      <h3 style="font-size: 1.5rem; font-weight: 800; margin-bottom: 12px; color: #f8fafc;">暮らしをスマートにする家電選びをサポート</h3>
      <p style="font-size: 0.95rem; color: #94a3b8; max-width: 600px; margin: 0 auto 24px; line-height: 1.7;">
        クラカジ編集部では、実際の楽天市場売れ筋データと仕様比較を徹底分析し、後悔しない家電選びの情報を発信しています。
      </p>
      <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
        <a href="/" style="background: #3b82f6; color: #fff; padding: 12px 28px; border-radius: 9999px; text-decoration: none; font-weight: 700; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 8px;">
          🏠 トップページへ戻る
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
      <div class="footer-links">
        <div class="footer-col">
          <h4>人気ランキング</h4>
          <ul>
            <li><a href="/articles/large-room-heater-best10.html">広い部屋用暖房器具TOP10</a></li>
            <li><a href="/articles/single-person-kotatsu-heater-best10.html">一人用こたつTOP10</a></li>
            <li><a href="/articles/wearable-blanket-rechargeable-warmer-best10.html">電気着る毛布＆充電カイロTOP10</a></li>
            <li><a href="/articles/desk-panel-heater-best10.html">デスク足元パネルヒーターTOP10</a></li>
            <li><a href="/articles/compact-futon-dryer-best10.html">コンパクト布団乾燥機TOP10</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>お役立ち検証・比較</h4>
          <ul>
            <li><a href="/articles/cluster/kotatsu-electricity-cost.html">一人用こたつの電気代検証</a></li>
            <li><a href="/articles/cluster/panel-heater-vs-ceramic.html">パネルヒーター vs セラミックヒーター</a></li>
            <li><a href="/articles/cluster/futon-dryer-dani-guide.html">布団乾燥機のダニ退治徹底ガイド</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p class="copyright">&copy; 2026 クラカジ (Kurakaji) All Rights Reserved.</p>
      </div>
    </div>
  </footer>
</body>
</html>
"""

print("Helper templates initialized.")
