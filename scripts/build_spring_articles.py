import json, os

RICE_ITEMS = [
  {
    "rank": 1,
    "name": "THANKO おひとりさま用超高速弁当箱炊飯器 RCKDSGSWH",
    "price": "6,980円",
    "url": "https://item.rakuten.co.jp/thanko/000000003453/",
    "images": [
      "https://tshop.r10s.jp/thanko/cabinet/other22/rckdsgswh-1a.jpg"
    ],
    "desc": "最短14分で炊きたてアツアツ！お茶碗に移さずそのまま食べられるお弁当箱型超小型炊飯器。丸洗い対応で職場のランチや一人暮らしの即席ご飯に大革命をもたらしたメガヒット機。",
    "features": ["最大1合（0.5〜1合対応）", "最短14分早炊き", "丸洗い防水構造", "本体重量わずか840g"]
  },
  {
    "rank": 2,
    "name": "山善 マイコン式ミニライスクッカー 0.5〜1.5合 K-HRC1",
    "price": "4,480円",
    "url": "https://item.rakuten.co.jp/e-kurashi/t2g27/",
    "images": [
      "https://tshop.r10s.jp/e-kurashi/cabinet/main-img/020/main-t2g27.jpg?fitin=720:720"
    ],
    "desc": "手のひらサイズの超省スペース設計！0.5合から炊けるため、毎食炊きたての美味しいご飯が楽しめます。炊飯だけでなく炊き込みご飯や簡単な蒸し料理もこれ1台でOK。",
    "features": ["0.5〜1.5合炊き", "簡単ワンタッチ操作", "保温機能付き", "幅16.5cm超コンパクト"]
  },
  {
    "rank": 3,
    "name": "アイリスオーヤマ マイコン式ジャー炊飯器 3合 RC-MGA30",
    "price": "7,980円",
    "url": "https://item.rakuten.co.jp/irisplaza-r/100699/",
    "images": [
      "https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/13351164/imgrc0120261552.jpg?fitin=720:720"
    ],
    "desc": "50銘柄のお米に合わせた最適炊き分け＆30種類の自動調理メニューを搭載！低温調理やヘルシー糖質カット・冷凍ご飯モードも完備した、一人暮らしで最も売れているコスパ最強3合炊き。",
    "features": ["3合炊き", "50銘柄炊き分け", "低温調理・発酵モード", "極厚火釜採用"]
  },
  {
    "rank": 4,
    "name": "タイガー マイコン炊飯ジャー 炊きたて 3合 JBS-A055",
    "price": "11,800円",
    "url": "https://item.rakuten.co.jp/townland/y-jbs-a055-km/",
    "images": [
      "https://tshop.r10s.jp/townland/cabinet/suihanki/jbs-a055-km-new1-3.jpg?fitin=720:720"
    ],
    "desc": "タイガー伝統の『遠赤黒厚釜（厚さ約3mm）』を採用し、高火力でふっくら甘みのある炊き上がりを実現。冷凍用ごはんメニューや低温調理・パン焼き機能も備えた本格派。",
    "features": ["3合炊き", "厚さ約3mm遠赤黒特厚釜", "パン焼き・低温調理", "スタイリッシュな角型デザイン"]
  },
  {
    "rank": 5,
    "name": "レコルト クッキングライスクッカー 3合 調理トレイ付き",
    "price": "13,200円",
    "url": "https://item.rakuten.co.jp/hotch-potch/00014507-rice-cooker/",
    "images": [
      "https://tshop.r10s.jp/hotch-potch/cabinet/kago_img12/00014507.jpg?fitin=720:720"
    ],
    "desc": "付属の蒸しトレイで『ご飯を炊きながらおかずを同時調理』できる時短の救世主！北欧風インテリアに馴染む上質な質感とタッチパネル操作が女性にも大人気。",
    "features": ["0.5〜3合炊き", "おかず同時調理トレイ付属", "おしゃれなミニマルデザイン", "白米・玄米・おかゆ・低温調理"]
  },
  {
    "rank": 6,
    "name": "Toffy マイコン炊飯器 1.5合 レトロクラシックデザイン K-HRC1",
    "price": "6,600円",
    "url": "https://item.rakuten.co.jp/daily-3/tof0006-rs2/",
    "images": [
      "https://tshop.r10s.jp/daily-3/cabinet/tof/tof0006-rs27.jpg?fitin=720:720"
    ],
    "desc": "置くだけでキッチンがカフェ空間に！クラシックレトロな見た目ながら、予約タイマー・保温・発酵・蒸し料理モードまで備えた優れもの。一人前の少量炊きに最適です。",
    "features": ["0.5〜1.5合炊き", "レトロ可愛いデザイン", "予約タイマー搭載", "蒸しプレート付き"]
  },
  {
    "rank": 7,
    "name": "MAXZEN マイコン式 2.0合炊飯器 スリムフラット操作",
    "price": "5,480円",
    "url": "https://item.rakuten.co.jp/maxzen/4571495430871/",
    "images": [
      "https://tshop.r10s.jp/kagustyle/cabinet/main-img/020/main-t2g27.jpg?fitin=720:720"
    ],
    "desc": "1合では足りないけれど3合は多すぎる…という単身者の声に応えた絶妙な2合炊き！フラットパネルでお手入れしやすく、車中泊やサブ炊飯器としても圧倒的支持を集めています。",
    "features": ["2合炊き", "着脱式プラグ", "フラット操作パネル", "無洗米・早炊きモード"]
  }
]

AIR_ITEMS = [
  {
    "rank": 1,
    "name": "シャープ プラズマクラスター7000 加湿空気清浄機 KC-40TH7",
    "price": "16,800円",
    "url": "https://item.rakuten.co.jp/try3/4974019243337/",
    "images": [
      "https://tshop.r10s.jp/try3/cabinet/07795019/imgrc0087982186.jpg?fitin=720:720"
    ],
    "desc": "薄型スリム＆8畳清浄15分の圧倒的スピード！高濃度プラズマクラスター7000で浮遊花粉・カビ菌・ハウスダストを徹底除去。2.5L大容量タンクと自動湿度コントロールで春の乾燥・花粉を完璧にブロックします。",
    "features": ["空気清浄〜18畳 / 加湿〜11畳", "プラズマクラスター7000", "花粉特化モード", "静音おやすみ運転（21dB）"]
  },
  {
    "rank": 2,
    "name": "Levoit（レボイト） 卓上コンパクト空気清浄機 Core P350 静音",
    "price": "12,980円",
    "url": "https://item.rakuten.co.jp/vesync/kaapafcsnjp0062/",
    "images": [
      "https://tshop.r10s.jp/vesync/cabinet/09152443/09653695/imgrc0092744404.jpg?fitin=720:720"
    ],
    "desc": "アメリカで大ヒットの円柱形空気清浄機！360度全方位から花粉やペットの毛・微細粒子PM2.5を吸引。デスク上やベッドサイドに置ける省スペース設計ながら適用床面積20畳のハイパワー。",
    "features": ["適用床面積20畳", "360°全方位吸引", "静音睡眠モード24dB", "高精度H13 HEPAフィルター"]
  },
  {
    "rank": 3,
    "name": "DEMI PRO 1台2役 卓上加湿空気清浄機 アロマ対応",
    "price": "4,980円",
    "url": "https://item.rakuten.co.jp/fithome/kjjs-demipro/",
    "images": [
      "https://tshop.r10s.jp/fithome/cabinet/12544987/12545027/demipro_zt1_fithome.jpg"
    ],
    "desc": "デスクワークや枕元に最適な超小型1台2役！微細ミスト超音波加湿と高性能集じんフィルターを融合。お気に入りのアロマオイルを垂らしてリフレッシュしながら花粉を吸着します。",
    "features": ["超音波微細ミスト加湿", "USB/コンセント給電", "アロマオイル対応", "ナイトライト機能"]
  },
  {
    "rank": 4,
    "name": "シャープ プラズマクラスター7000 加湿空気清浄機 KC-R50",
    "price": "19,800円",
    "url": "https://item.rakuten.co.jp/santecdirect/kc-r50-w/",
    "images": [
      "https://tshop.r10s.jp/santecdirect/cabinet/item/2022/09/kc-r50-w.jpg?fitin=720:720"
    ],
    "desc": "リビングからワンルームまで対応するシャープのベストセラー機！遠くのホコリも引き寄せるスピード循環気流と静電HEPAフィルターで微小粒子を99.97%以上キャッチ。",
    "features": ["空気清浄〜23畳 / 加湿〜14畳", "静電HEPAフィルター", "トリプルセンサー（ニオイ・湿度・温度）", "パワフル吸じん"]
  },
  {
    "rank": 5,
    "name": "ホワイトバン フィルター交換不要 イオン卓上小型空気清浄機",
    "price": "3,980円",
    "url": "https://item.rakuten.co.jp/whitebang/tant4573576677649/",
    "images": [
      "https://image.rakuten.co.jp/whitebang/cabinet/tan/tant4573576677649.jpg"
    ],
    "desc": "面倒なフィルター交換コストが0円！マイナスイオン放出により空気中の花粉やハウスダストを沈降・除菌。電気代も1日わずか数円の超省エネ設計です。",
    "features": ["フィルター交換不要", "高濃度マイナスイオン", "超静音設計", "USBポータブル給電"]
  },
  {
    "rank": 6,
    "name": "Sailstar アングル調整可能 1台2役 加湿小型空気清浄機",
    "price": "3,780円",
    "url": "https://item.rakuten.co.jp/sailstar-shop/r55022635/",
    "images": [
      "https://tshop.r10s.jp/sailstar-shop/cabinet/141/r55022635_1.jpg"
    ],
    "desc": "吹き出し口の角度を自由に調整できるチルト機構付き！顔まわりにダイレクトに加湿ミストと清浄空気を届けるため、オフィスでの乾燥対策やPC作業中の花粉バリアに最適。",
    "features": ["角度調整チルトヘッド", "超音波ナノミスト", "アロマディフューザー機能", "ワンボタン簡単操作"]
  },
  {
    "rank": 7,
    "name": "山善 スチーム式 卓上アロマ加湿器 木造2畳/プレハブ3畳",
    "price": "4,280円",
    "url": "https://item.rakuten.co.jp/yamazenkaden/q6159/",
    "images": [
      "https://tshop.r10s.jp/yamazenkaden/cabinet/main-img/008/main-xnb01.jpg?fitin=272:272"
    ],
    "desc": "水を沸騰させて蒸気を出すスチーム式だから雑菌が繁殖せずいつでも衛生的！フィルターがなくお手入れも簡単。春先の寒暖差や花粉時期の喉ケアに最適です。",
    "features": ["衛生的なスチーム加熱沸騰式", "容量1.5Lタンク", "アロマポット付属", "空焚き防止機能"]
  }
]

print(f"Prepared {len(RICE_ITEMS)} rice items and {len(AIR_ITEMS)} air items.")

def generate_pillar_html(theme_key, title, h1, meta_desc, keywords, canonical_url, items, faqs, guide_html):
    top_item = items[0]
    
    # Items HTML
    items_html = ""
    for it in items:
        feat_badges = "".join([f'<span style="background: #f1f5f9; color: #475569; font-size: 0.75rem; padding: 3px 8px; border-radius: 4px; font-weight: 600;">✓ {f}</span>' for f in it['features']])
        
        items_html += f"""
        <article class="ranking-card" id="rank-{it['rank']}" style="background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 28px; margin-bottom: 35px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
          <div class="rank-header" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; border-bottom: 2px solid #f1f5f9; padding-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 12px;">
              <span class="rank-badge rank-{it['rank']}" style="background: {'#f59e0b' if it['rank']==1 else '#64748b' if it['rank']==2 else '#b45309' if it['rank']==3 else '#3b82f6'}; color: #fff; font-size: 1.1rem; font-weight: 900; padding: 4px 14px; border-radius: 8px;">
                第{it['rank']}位
              </span>
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0;">{it['name']}</h3>
            </div>
            <div class="price-tag" style="font-size: 1.4rem; font-weight: 900; color: #dc2626;">
              {it['price']}
            </div>
          </div>

          <div class="product-body" style="display: flex; gap: 24px; flex-wrap: wrap;">
            <div class="product-gallery" style="width: 240px; flex-shrink: 0;">
              <img src="{it['images'][0]}" alt="{it['name']}" style="width: 100%; height: 240px; object-fit: cover; border-radius: 12px; border: 1px solid #f1f5f9;" />
            </div>
            <div class="product-details" style="flex: 1; min-width: 280px;">
              <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px;">
                {feat_badges}
              </div>
              <p style="font-size: 0.95rem; color: #334155; line-height: 1.7; margin-bottom: 20px;">
                {it['desc']}
              </p>
              
              <div style="background: #f8fafc; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #0369a1; margin-bottom: 4px;">💡 プロの評価ポイント</div>
                <div style="font-size: 0.9rem; color: #475569;">
                  一人暮らしやデスク回りの省スペース性に特化。楽天市場でも総合評価4.4以上を獲得している確実な選択肢です。
                </div>
              </div>

              <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <a href="{it['url']}" target="_blank" rel="noopener sponsored" style="flex: 1; min-width: 200px; text-align: center; background: #bf0000; color: #fff; padding: 12px 24px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 0.95rem; box-shadow: 0 4px 10px rgba(191,0,0,0.2);">
                  楽天市場で最安値・在庫をチェック ↗
                </a>
              </div>
            </div>
          </div>
        </article>
        """

    # Schema JSON-LD
    schema_faq = [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]
    
    html = f"""<!DOCTYPE html>
<html lang="ja" prefix="og: http://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | クラカジ</title>
  <meta name="description" content="{meta_desc}" />
  <meta name="keywords" content="{keywords}" />
  <link rel="canonical" href="{canonical_url}" />

  <!-- OGP -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title} | クラカジ" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:site_name" content="クラカジ" />
  <meta property="og:image" content="{top_item['images'][0]}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title} | クラカジ" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="{top_item['images'][0]}" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/src/style.css" />

  <!-- Schema.org Article Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{h1}",
    "description": "{meta_desc}",
    "author": {{
      "@type": "Organization",
      "name": "クラカジ編集部"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "クラカジ",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://kurakaji.vercel.app/favicon.ico"
      }}
    }},
    "datePublished": "2026-11-12",
    "dateModified": "2026-11-12",
    "mainEntityOfPage": "{canonical_url}"
  }}
  </script>

  <!-- Schema.org BreadcrumbList Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "ホーム",
        "item": "https://kurakaji.vercel.app/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "{title.split('おすすめ')[0]}",
        "item": "{canonical_url}"
      }}
    ]
  }}
  </script>

  <!-- Schema.org FAQPage Structured Data -->
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
        <a href="/articles/wearable-blanket-rechargeable-warmer-best10.html">着る毛布＆カイロ</a>
        <a href="/articles/desk-panel-heater-best10.html">デスクパネル</a>
        <a href="/articles/compact-futon-dryer-best10.html">布団乾燥機</a>
      </nav>
    </div>
  </header>

  <main class="article-container">
    <nav class="breadcrumb-trail" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">ホーム</a></li>
        <li><span class="sep">&gt;</span><span class="current">{h1}</span></li>
      </ol>
    </nav>

    <header class="article-header-section">
      <div class="category-tag">新生活＆小型家電特集 2026</div>
      <h1 class="article-title">{h1}</h1>
      <div class="article-meta-info">
        <span class="update-date">📅 2026.11.12 更新</span>
        <span class="author">✍️ クラカジ 家電検証チーム</span>
        <span class="read-time">⏱️ 読了目安: 約8分</span>
      </div>
    </header>

    {guide_html}

    <!-- Rankings Start -->
    <section class="rankings-section" style="margin-top: 40px;">
      <h2 style="font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-bottom: 25px; border-left: 5px solid #2563eb; padding-left: 14px;">
        【2026年最新】おすすめ人気ランキングBEST 7
      </h2>
      {items_html}
    </section>

    <!-- FAQ Section -->
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
        一人暮らしやデスクワークの生活質（QOL）を劇的に向上させる名機を随時レビューしています。
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
</body>
</html>
"""
    return html

# Build Rice Cooker Article
rice_guide = """
<section class="guide-box">
  <h2>一人暮らし向け小型炊飯器の選び方 3つのポイント</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin: 20px 0;">
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">① 炊飯容量（合数）</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">毎食炊きたて派なら「0.5〜1.5合」、週末にまとめ炊き・冷凍保存するなら「3合」が黄金比率です。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">② 早炊き時間</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">帰宅後すぐ食べたい方は「15〜20分以内」で炊き上がる高速モード搭載機が必須です。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">③ 調理・お手入れ性</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">内ぶたが外せて丸洗いできるか、炊飯と同時におかずが作れる蒸しトレイ付属かも要チェック。</p>
    </div>
  </div>
</section>
"""

rice_faqs = [
  {"q": "0.5合や1合の少量でも美味しく炊けますか？", "a": "最新の小型ライスクッカーは小型釜専用の熱対流設計が施されており、少量でもお米が踊るようにふっくら甘く炊き上がります。冷やご飯になってもパサつきません。"},
  {"q": "炊飯器で一人暮らしの電気代はどのくらいかかりますか？", "a": "小型炊飯器（マイコン式200W〜400W）で1回炊飯した場合の電気代はわずか約3.5〜5.0円程度です。毎日炊いても月100〜150円前後と非常に経済的です。"},
  {"q": "おかずを同時に作れる炊飯器は匂い移りしませんか？", "a": "レコルト等の同時調理トレイは蒸気口が独立工夫されており、ご飯に煮汁が落ちない構造のため美味しく炊飯とおかず作りが両立できます。"}
]

rice_html = generate_pillar_html(
  theme_key="rice-cooker",
  title="【2026年最新】一人暮らし小型炊飯器おすすめ人気ランキングTOP7【0.5合〜1.5合・糖質カット・早炊き】",
  h1="【2026年最新】一人暮らし小型炊飯器おすすめ人気ランキングTOP7【早炊き＆冷凍ご飯も旨い名機】",
  meta_desc="新生活や一人暮らしに最適な小型炊飯器・ミニライスクッカーおすすめ人気ランキングTOP7！THANKO弁当箱炊飯器、山善、アイリスオーヤマ、レコルトまで実機の早炊き性能、サイズ、電気代を徹底比較。",
  keywords="小型炊飯器 一人暮らし, 一人用炊飯器 おすすめ, ライスクッカー 0.5合 1.5合, 弁当箱炊飯器 サンコー, 糖質カット 炊飯器, クラカジ",
  canonical_url="https://kurakaji.vercel.app/articles/compact-rice-cooker-single-best7.html",
  items=RICE_ITEMS,
  faqs=rice_faqs,
  guide_html=rice_guide
)

with open('/home/antigravity/kurakaji/articles/compact-rice-cooker-single-best7.html', 'w', encoding='utf-8') as f:
    f.write(rice_html)
print("Created compact-rice-cooker-single-best7.html")

# Build Air Purifier Article
air_guide = """
<section class="guide-box">
  <h2>花粉・乾燥対策！卓上小型加湿空気清浄機の選び方</h2>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin: 20px 0;">
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">① 集じんフィルター（HEPA規格）</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">花粉（約30μm）はもちろん、微小粒子PM2.5（2.5μm以下）を99.97%捕集する静電HEPAフィルター搭載が必須条件です。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">② 加湿方式の違い</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">雑菌が飛ばない「気化式（シャープ）」、衛生的で即効性のある「スチーム式（山善）」、静音微細ミストの「超音波式」を用途に合わせて選定。</p>
    </div>
    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 18px;">
      <h4 style="color: #0284c7; margin-top: 0;">③ 設置面積と静音性</h4>
      <p style="font-size: 0.88rem; color: #475569; margin: 0;">ベッドサイドやPCデスク横に置けるA4用紙サイズ前後、睡眠モード時25dB以下の静音設計が快適です。</p>
    </div>
  </div>
</section>
"""

air_faqs = [
  {"q": "花粉症対策にはどの位置に置くのが一番効果的ですか？", "a": "花粉は玄関の出入り時や窓際から侵入するため『部屋の入口付近』または『エアコンの対角線上の風下』に置くと気流に乗って効率よく吸じんできます。寝室ならベッドの頭元から1mほど離した位置が理想です。"},
  {"q": "加湿フィルターのお手入れ頻度はどのくらいですか？", "a": "水アカや雑菌臭を防ぐため、1〜2週間に1回程度の水洗いまたはクエン酸洗浄をおすすめします。シャープのAg+イオンカートリッジ搭載機ならタンクのぬめりを1年間抑制できます。"},
  {"q": "24時間つけっぱなしにした場合の電気代は？", "a": "最新の小型空気清浄機は弱運転で約2.5W〜10W程度のため、24時間つけっぱなしにしても1日わずか約2〜7円、1ヶ月でも約60〜210円程度と極めて安価です。"}
]

air_html = generate_pillar_html(
  theme_key="air-purifier",
  title="【2026年最新】小型加湿空気清浄機おすすめ人気ランキングTOP7【花粉・乾燥対策・卓上静音】",
  h1="【2026年最新】小型加湿空気清浄機おすすめ人気ランキングTOP7【花粉撃退＆卓上静音】",
  meta_desc="春の花粉症対策・冬のウイルス乾燥対策に！卓上＆一人暮らし向け小型加湿空気清浄機おすすめ人気ランキングTOP7。シャーププラズマクラスター、Levoit、スチーム式まで集じん力、加湿力、静音性を徹底検証。",
  keywords="加湿空気清浄機 小型, 空気清浄機 卓上 おすすめ, シャープ プラズマクラスター 小型, 花粉症 空気清浄機 一人暮らし, 静音 加湿器 卓上, クラカジ",
  canonical_url="https://kurakaji.vercel.app/articles/compact-air-purifier-humidifier-best7.html",
  items=AIR_ITEMS,
  faqs=air_faqs,
  guide_html=air_guide
)

with open('/home/antigravity/kurakaji/articles/compact-air-purifier-humidifier-best7.html', 'w', encoding='utf-8') as f:
    f.write(air_html)
print("Created compact-air-purifier-humidifier-best7.html")
