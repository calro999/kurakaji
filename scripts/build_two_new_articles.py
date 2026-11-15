import json, os, re
from new_expansions_data import NEW_EXPANSIONS

with open('/home/antigravity/kurakaji/scripts/verified_20_new_items.json', 'r', encoding='utf-8') as f:
    all_items = json.load(f)

# Group by theme
themes = {
    'panel-heater': {
        'filepath': '/home/antigravity/kurakaji/articles/desk-panel-heater-best10.html',
        'items': [it for it in all_items if it['theme'] == 'panel-heater']
    },
    'futon-dryer': {
        'filepath': '/home/antigravity/kurakaji/articles/compact-futon-dryer-best10.html',
        'items': [it for it in all_items if it['theme'] == 'futon-dryer']
    }
}

SEO_META = {
  "panel-heater": {
    "h1": "【2026年最新】デスク下足元パネルヒーターおすすめ人気ランキングTOP10【電気代1時間5円！冷え性撃退の神機】",
    "meta_desc": "在宅ワークやオフィスのデスク下に置くだけで足元から極楽！5面発熱・ラウンド型・折りたたみ遠赤外線デスクパネルヒーターおすすめ人気ランキングTOP10。1時間の電気代比較、安全性、選び方をプロが徹底検証。",
    "keywords": "デスク パネルヒーター, パネルヒーター 足元 おすすめ, デスクヒーター 遠赤外線, パネルヒーター 電気代 比較, 折りたたみ 足元ヒーター, 2026 クラカジ",
    "breadcrumb_name": "デスクパネルヒーターTOP10",
    "faq": [
      {
        "q": "パネルヒーターの1ヶ月の電気代はいくらですか？",
        "a": "一般的なデスクパネルヒーター（約190W）を1日8時間使用した場合、1時間あたり約4.5〜5.5円、1ヶ月（30日）使用してもわずか約1,000〜1,300円程度です。エアコン暖房をつけっぱなしにする場合（月5,000〜8,000円）と比べて約80%以上の電気代削減になります。"
      },
      {
        "q": "3面タイプと5面タイプ、ラウンド型はどれがおすすめですか？",
        "a": "床面からの底冷えが厳しい場合は『底面ヒーター付きの5面タイプ』、隙間風を完全にシャットアウトしたい場合は『360度ラウンド型』が最適です。手軽に出し入れしたい場合は軽量な3面タイプが扱いやすくおすすめです。"
      },
      {
        "q": "オフィスや集合住宅で使っても音や匂いは気になりませんか？",
        "a": "パネルヒーターはファンがないため稼働音は完全な無音（0dB）です。また温風を出さない遠赤外線輻射熱のため、ホコリやハウスダストを巻き上げず、喉や目が乾燥する心配も一切ありません。"
      }
    ],
    "guide_section": """
    <section class="guide-box">
      <h2>🏆 デスクパネルヒーター選びで絶対に失敗しない「4つの検証基準」</h2>
      <div class="guide-grid">
        <div class="guide-card">
          <div class="guide-num">01</div>
          <h3>「底面発熱（足裏ヒーター）」の有無</h3>
          <p>足元の冷えの8割は床からの『底冷え』が原因。底面にもヒーターパネルが内蔵されている5面タイプやラウンド型を選ぶことで、足裏からじわじわと温まり体感温度が段違いに跳ね上がります。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">02</div>
          <h3>隙間風を防ぐ「ラウンド構造・天板毛布」</h3>
          <p>前面や側面だけでなく、背面や上部からの熱逃げを防ぐカバーやラウンド型構造なら、熱効率が2倍以上に向上。弱運転でも十分な温かさを保てるためさらなる節電に繋がります。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">03</div>
          <h3>自動電源オフ（消し忘れ防止タイマー）</h3>
          <p>退勤時や外出時にうっかり電源を切り忘れても安心な2〜8時間の自動OFFタイマー、および足がぶつかって45度以上傾いた際に瞬時に通電を切る転倒防止センサーは必須です。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">04</div>
          <h3>折りたたみ時の厚みと収納性</h3>
          <p>オフシーズンや掃除の際、厚さ3〜5cm程度にフラットに折りたためるモデルなら、デスクの隙間や本棚の横にスッと収納でき、部屋の生活感を邪魔しません。</p>
        </div>
      </div>
    </section>

    <!-- Comparison Table Section -->
    <section class="compare-table-box">
      <h2>📊 デスクパネルヒーター 形状・電気代早見比較表</h2>
      <div class="table-responsive">
        <table class="styled-table">
          <thead>
            <tr>
              <th>順位 / モデル名</th>
              <th>タイプ・形状</th>
              <th>消費電力</th>
              <th>電気代目安(時)</th>
              <th>参考価格</th>
            </tr>
          </thead>
          <tbody>
            <tr class="highlight">
              <td><strong>第1位：遠赤外線 5面発熱モデル</strong></td>
              <td>5面立体（底面発熱付）</td>
              <td>195W</td>
              <td>約5.0円</td>
              <td>4,980円</td>
            </tr>
            <tr>
              <td><strong>第2位：360°ラウンド型 円柱ヒーター</strong></td>
              <td>円筒ラウンド（毛布付）</td>
              <td>185W</td>
              <td>約4.8円</td>
              <td>5,480円</td>
            </tr>
            <tr>
              <td><strong>第3位：NooQ ヌーク 北欧パネル</strong></td>
              <td>5面洗練ファブリック</td>
              <td>190W</td>
              <td>約4.6円</td>
              <td>7,980円</td>
            </tr>
            <tr>
              <td><strong>第4位：Wishsun 6段階温度調節</strong></td>
              <td>4面ワイド（LED表示）</td>
              <td>195W</td>
              <td>約5.0円</td>
              <td>4,580円</td>
            </tr>
            <tr>
              <td><strong>第5位：ROSIDA 2WAYホットマット兼用</strong></td>
              <td>立つ・寝る2WAY変形</td>
              <td>180W</td>
              <td>約4.2円</td>
              <td>6,280円</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
  },

  "futon-dryer": {
    "h1": "【2026年最新】コンパクト布団乾燥機おすすめ人気ランキングTOP10【マット不要・ダニ撃退＆靴乾燥】",
    "meta_desc": "冬の冷たい布団を一瞬でホカホカ極楽に変える！アイリスオーヤマ カラリエ、ツインノズル、衣類乾燥袋付きおすすめコンパクト布団乾燥機人気ランキングTOP10。ダニ退治、梅雨・花粉時の靴乾燥まで徹底比較検証。",
    "keywords": "布団乾燥機 おすすめ, カラリエ アイリスオーヤマ, 布団乾燥機 コンパクト, 布団乾燥機 靴乾燥, ダニ退治 布団乾燥機, 2026 クラカジ",
    "breadcrumb_name": "コンパクト布団乾燥機TOP10",
    "faq": [
      {
        "q": "布団乾燥機の電気代は1回あたりいくらですか？",
        "a": "冬のあたためモード（約20分）で使用した場合、1回あたりの電気代はわずか約6〜8円程度です。毎日寝る前に使っても1ヶ月約200円前後と、コインランドリーの大型乾燥機（1回300〜500円）を利用するのと比べて劇的な節約になります。"
      },
      {
        "q": "ツインノズルとシングルノズルはどちらを選ぶべきですか？",
        "a": "ご家族で布団を2組並べて寝ている方や、ダブル・クイーンサイズの大きめベッドをお使いの方は『ツインノズル』が圧倒的に時短でおすすめです。一人暮らしやシングルベッドであれば、軽量で場所を取らない『シングルノズル』で十分満足いただけます。"
      },
      {
        "q": "雨で濡れた靴やスニーカーも乾かせますか？",
        "a": "はい、今回ご紹介しているランキング上位モデルにはすべて専用の『くつ乾燥アタッチメント』が付属しています。濡れたスニーカーなら約30〜50分で内側までカラッと乾かすことができます。"
      }
    ],
    "guide_section": """
    <section class="guide-box">
      <h2>🏆 布団乾燥機選びで後悔しないための「4つの重要チェック」</h2>
      <div class="guide-grid">
        <div class="guide-card">
          <div class="guide-num">01</div>
          <h3>「マット不要＆ノズル差し込み式」一択</h3>
          <p>昔のような面倒なエアマットを広げる必要は一切ありません。ホースを伸ばして布団に差し込むだけで準備完了するノズル式を選ぶことが、毎日ストレスなく使い続ける最大の秘訣です。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">02</div>
          <h3>立体ノズル（フラップ付き）の有無</h3>
          <p>ノズルの先端に立ち上がる立体フラップが付いていると、重い掛け布団を持ち上げて大きな温風空間を形成。足元から胸元、布団の端まで均一に熱が行き渡ります。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">03</div>
          <h3>靴・衣類乾燥アタッチメントの付属</h3>
          <p>雨の日や雪の日にびしょ濡れになった靴、梅雨時の部屋干し洗濯物もカラッと乾かせるアタッチメント付きモデルなら、冬の防寒だけでなく1年中365日フル稼働できます。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">04</div>
          <h3>出しっぱなしにできるコンパクトデザイン</h3>
          <p>ベッドサイドやクローゼットの隙間に収まるスリム・軽量設計（2kg前後）なら、出し入れの億劫さがゼロ。寝る前の15分習慣が驚くほど定着します。</p>
        </div>
      </div>
    </section>

    <!-- Comparison Table Section -->
    <section class="compare-table-box">
      <h2>📊 布団乾燥機 性能・機能早見比較表</h2>
      <div class="table-responsive">
        <table class="styled-table">
          <thead>
            <tr>
              <th>順位 / モデル名</th>
              <th>ノズルタイプ</th>
              <th>主要機能</th>
              <th>重量</th>
              <th>参考価格</th>
            </tr>
          </thead>
          <tbody>
            <tr class="highlight">
              <td><strong>第1位：カラリエ ツインノズル FK-W2</strong></td>
              <td>ツインノズル</td>
              <td>布団2組同時 / 靴乾燥 / ダニ退治</td>
              <td>約2.2kg</td>
              <td>13,800円</td>
            </tr>
            <tr>
              <td><strong>第2位：カラリエ mini TURBO</strong></td>
              <td>ツインノズル</td>
              <td>超速暖3分半 / 北欧木目調デザイン</td>
              <td>約2.1kg</td>
              <td>14,080円</td>
            </tr>
            <tr>
              <td><strong>第3位：カラリエ シングルノズル</strong></td>
              <td>シングルノズル</td>
              <td>軽量1.8kg / シンプル3秒セット</td>
              <td>約1.8kg</td>
              <td>8,980円</td>
            </tr>
            <tr>
              <td><strong>第4位：カラリエ ハイパワー＋衣類乾燥袋</strong></td>
              <td>ハイパワー900W</td>
              <td>部屋干し衣類60分乾燥カバー付</td>
              <td>約2.4kg</td>
              <td>16,800円</td>
            </tr>
            <tr>
              <td><strong>第5位：パナソニック ナノイー搭載</strong></td>
              <td>ロング立体ノズル</td>
              <td>ナノイー頭皮臭・加齢臭脱臭</td>
              <td>約2.8kg</td>
              <td>22,780円</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
  }
}

ADVANCED_CSS = """
    /* Breadcrumbs Navigation */
    .breadcrumb-nav {
      font-size: 0.85rem;
      color: var(--color-text-muted);
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.5rem;
    }
    .breadcrumb-nav a {
      color: var(--color-brand-primary);
      text-decoration: none;
      font-weight: 600;
    }
    .breadcrumb-nav a:hover {
      text-decoration: underline;
    }
    .breadcrumb-separator {
      color: #94a3b8;
    }

    /* Rich Article Typography & Layout */
    .article-container {
      max-width: 880px;
      margin: 0 auto;
      padding: 2rem 1.25rem 5rem;
    }
    .article-header {
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--color-border);
      padding-bottom: 2rem;
    }
    .article-tag {
      display: inline-block;
      padding: 0.35rem 0.9rem;
      border-radius: var(--radius-full);
      background-color: var(--color-brand-light);
      color: var(--color-brand-primary);
      font-size: 0.82rem;
      font-weight: 800;
      margin-bottom: 1rem;
      border: 1px solid rgba(13, 148, 136, 0.2);
    }
    .article-h1 {
      font-size: 1.95rem;
      font-weight: 800;
      line-height: 1.45;
      color: var(--color-text-main);
      margin-bottom: 1.2rem;
    }
    .article-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 1.25rem;
      font-size: 0.85rem;
      color: var(--color-text-muted);
      margin-bottom: 1.5rem;
    }
    .article-lead {
      font-size: 1.05rem;
      line-height: 1.8;
      color: #334155;
      background: #ffffff;
      padding: 1.75rem;
      border-radius: var(--radius-md);
      border-left: 5px solid var(--color-brand-primary);
      box-shadow: var(--shadow-sm);
    }

    /* Buying Guide Section */
    .guide-box {
      background: #ffffff;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: 2rem;
      margin: 2.5rem 0;
      box-shadow: var(--shadow-sm);
    }
    .guide-box h2 {
      font-size: 1.35rem;
      font-weight: 800;
      margin-bottom: 1.5rem;
      border-bottom: 2px solid var(--color-brand-primary);
      padding-bottom: 0.5rem;
      color: var(--color-text-main);
    }
    .guide-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1.25rem;
    }
    .guide-card {
      background: #f8fafc;
      padding: 1.25rem;
      border-radius: var(--radius-md);
      border: 1px solid var(--color-border);
    }
    .guide-num {
      display: inline-block;
      font-family: var(--font-en);
      font-weight: 900;
      font-size: 1.3rem;
      color: var(--color-brand-primary);
      margin-bottom: 0.4rem;
    }
    .guide-card h3 {
      font-size: 1.05rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
      color: var(--color-text-main);
    }
    .guide-card p {
      font-size: 0.9rem;
      color: #475569;
      line-height: 1.65;
    }

    /* Comparison Table Section */
    .compare-table-box {
      background: #ffffff;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: 2rem;
      margin: 2.5rem 0;
      box-shadow: var(--shadow-sm);
    }
    .compare-table-box h2 {
      font-size: 1.35rem;
      font-weight: 800;
      margin-bottom: 1.25rem;
      color: var(--color-text-main);
      border-bottom: 2px solid var(--color-brand-primary);
      padding-bottom: 0.5rem;
    }
    .table-responsive {
      overflow-x: auto;
    }
    .styled-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
      text-align: left;
    }
    .styled-table th {
      background: #f1f5f9;
      color: #1e293b;
      padding: 0.75rem 1rem;
      font-weight: 700;
      border-bottom: 2px solid var(--color-border);
      white-space: nowrap;
    }
    .styled-table td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--color-border);
      color: #334155;
    }
    .styled-table tr.highlight {
      background: #f0fdfa;
      font-weight: 600;
    }

    /* TOC Box */
    .toc-box {
      background: #f8fafc;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-md);
      padding: 1.5rem;
      margin: 2.5rem 0;
    }
    .toc-title {
      font-weight: 800;
      font-size: 1.05rem;
      color: var(--color-text-main);
      margin-bottom: 0.75rem;
    }
    .toc-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .toc-list a {
      color: #0369a1;
      text-decoration: none;
      font-size: 0.92rem;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
    }
    .toc-list a:hover {
      text-decoration: underline;
      color: var(--color-brand-primary);
    }

    /* Product Ranking Cards */
    .rank-card {
      background: #ffffff;
      border-radius: var(--radius-lg);
      border: 1.5px solid var(--color-border);
      padding: 2.25rem;
      margin-bottom: 3rem;
      box-shadow: var(--shadow-sm);
      scroll-margin-top: 5rem;
    }
    .rank-badge-wrap {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1rem;
    }
    .rank-badge {
      width: 48px;
      height: 48px;
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-en);
      font-size: 1.35rem;
      font-weight: 900;
      background: #e2e8f0;
      color: #334155;
    }
    .rank-badge.top1 {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #ffffff;
      box-shadow: 0 4px 10px rgba(245, 158, 11, 0.35);
    }
    .rank-badge.top2 {
      background: linear-gradient(135deg, #94a3b8, #64748b);
      color: #ffffff;
    }
    .rank-badge.top3 {
      background: linear-gradient(135deg, #b45309, #78350f);
      color: #ffffff;
    }
    .rank-badge-label {
      font-size: 0.85rem;
      font-weight: 800;
      color: var(--color-brand-primary);
    }
    .rank-item-title {
      font-size: 1.45rem;
      font-weight: 800;
      line-height: 1.45;
      color: var(--color-text-main);
      margin-bottom: 1.25rem;
    }

    /* 3-Images Responsive Gallery */
    .rank-gallery {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.75rem;
      margin-bottom: 1.5rem;
    }
    .rank-gallery img {
      width: 100%;
      height: 200px;
      object-fit: cover;
      background: #f8fafc;
      border-radius: var(--radius-sm);
      border: 1px solid var(--color-border);
      padding: 0.4rem;
      transition: transform 0.2s;
    }
    .rank-gallery img:hover {
      transform: scale(1.03);
    }

    /* Verification & Deep Review Box */
    .deep-review-box {
      background: #f8fafc;
      border-radius: var(--radius-md);
      border: 1px solid var(--color-border);
      padding: 1.5rem;
      margin-bottom: 1.5rem;
    }
    .deep-review-box h4 {
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--color-text-main);
      margin-bottom: 0.6rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .deep-review-box p {
      font-size: 0.95rem;
      line-height: 1.75;
      color: #334155;
    }

    /* Merits & Demerits Grid */
    .pros-cons-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .pros-box {
      background: #f0fdf4;
      border: 1px solid #bbf7d0;
      border-radius: var(--radius-md);
      padding: 1.25rem;
    }
    .pros-box h5 {
      font-size: 0.95rem;
      font-weight: 800;
      color: #166534;
      margin-bottom: 0.6rem;
    }
    .pros-box ul, .cons-box ul {
      list-style: none;
      font-size: 0.88rem;
      color: #1f2937;
      line-height: 1.6;
    }
    .pros-box li::before {
      content: "✔ ";
      color: #16a34a;
      font-weight: 800;
    }
    .cons-box {
      background: #fff1f2;
      border: 1px solid #fecdd3;
      border-radius: var(--radius-md);
      padding: 1.25rem;
    }
    .cons-box h5 {
      font-size: 0.95rem;
      font-weight: 800;
      color: #9f1239;
      margin-bottom: 0.6rem;
    }
    .cons-box li::before {
      content: "▲ ";
      color: #e11d48;
      font-weight: 800;
    }

    /* User Voice Box */
    .user-voice-box {
      background: #eff6ff;
      border-left: 4px solid #3b82f6;
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
      padding: 1rem 1.25rem;
      font-size: 0.9rem;
      line-height: 1.65;
      color: #1e3a8a;
      margin-bottom: 1.5rem;
    }

    .specs-list {
      list-style: none;
      background: #f8fafc;
      padding: 1rem 1.25rem;
      border-radius: var(--radius-sm);
      margin-bottom: 1.5rem;
      font-size: 0.88rem;
      color: #334155;
    }
    .specs-list li {
      margin-bottom: 0.35rem;
    }

    .rank-cta-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 1rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--color-border);
    }
    .rank-price {
      font-size: 1.45rem;
      font-weight: 900;
      color: var(--color-cta);
    }
    .rank-cta-btn {
      background: var(--color-cta);
      color: #ffffff;
      padding: 0.85rem 2rem;
      border-radius: var(--radius-full);
      font-weight: 800;
      font-size: 0.98rem;
      box-shadow: 0 4px 14px rgba(225, 29, 72, 0.28);
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      text-decoration: none;
    }
    .rank-cta-btn:hover {
      background: var(--color-cta-hover);
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(225, 29, 72, 0.38);
    }

    /* FAQ Accordion Section */
    .faq-box {
      background: #ffffff;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: 2rem;
      margin: 3.5rem 0;
      box-shadow: var(--shadow-sm);
    }
    .faq-box h2 {
      font-size: 1.35rem;
      font-weight: 800;
      margin-bottom: 1.5rem;
      border-bottom: 2px solid var(--color-brand-primary);
      padding-bottom: 0.5rem;
      color: var(--color-text-main);
    }
    .faq-item {
      margin-bottom: 1.25rem;
      border-bottom: 1px solid var(--color-border);
      padding-bottom: 1.25rem;
    }
    .faq-item:last-child {
      border-bottom: none;
      margin-bottom: 0;
      padding-bottom: 0;
    }
    .faq-q {
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--color-text-main);
      margin-bottom: 0.5rem;
      display: flex;
      gap: 0.5rem;
      align-items: baseline;
    }
    .faq-q span {
      color: var(--color-brand-primary);
      font-size: 1.2rem;
    }
    .faq-a {
      font-size: 0.92rem;
      color: #475569;
      line-height: 1.7;
      padding-left: 1.7rem;
    }

    @media (max-width: 640px) {
      .article-h1 {
        font-size: 1.45rem;
      }
      .rank-item-title {
        font-size: 1.15rem;
      }
      .rank-card {
        padding: 1.25rem;
      }
      .rank-gallery {
        grid-template-columns: repeat(3, 1fr);
        gap: 0.4rem;
      }
      .rank-gallery img {
        height: 100px;
      }
      .rank-cta-btn {
        width: 100%;
        justify-content: center;
      }
    }
"""

for theme_id, tdata in themes.items():
    filepath = tdata['filepath']
    items = tdata['items']
    meta = SEO_META[theme_id]
    expansions = NEW_EXPANSIONS.get(theme_id, [])

    # Build schema.org JSON-LD
    faq_schema_list = []
    for f in meta['faq']:
        faq_schema_list.append({
          "@type": "Question",
          "name": f['q'],
          "acceptedAnswer": {
            "@type": "Answer",
            "text": f['a']
          }
        })

    canonical_url = filepath.replace('/home/antigravity/kurakaji', 'https://kurakaji.vercel.app')

    json_ld_article = {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": meta['h1'],
      "description": meta['meta_desc'],
      "author": {
        "@type": "Organization",
        "name": "クラカジ編集部"
      },
      "publisher": {
        "@type": "Organization",
        "name": "クラカジ",
        "logo": {
          "@type": "ImageObject",
          "url": "https://kurakaji.vercel.app/favicon.ico"
        }
      },
      "datePublished": "2026-11-12",
      "dateModified": "2026-11-12",
      "mainEntityOfPage": canonical_url
    }

    json_ld_breadcrumb = {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "ホーム",
          "item": "https://kurakaji.vercel.app/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "冬の季節家電特集",
          "item": "https://kurakaji.vercel.app/#editorial"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": meta['breadcrumb_name'],
          "item": canonical_url
        }
      ]
    }

    first_img = items[0]['images'][0] if items and items[0]['images'] else ''

    html = f'''<!DOCTYPE html>
<html lang="ja" prefix="og: http://ogp.me/ns#">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{meta['h1']} | クラカジ</title>
  <meta name="description" content="{meta['meta_desc']}" />
  <meta name="keywords" content="{meta['keywords']}" />
  <link rel="canonical" href="{canonical_url}" />

  <!-- OGP -->
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{meta['h1']}" />
  <meta property="og:description" content="{meta['meta_desc']}" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:site_name" content="クラカジ" />
  <meta property="og:image" content="{first_img}" />

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{meta['h1']}" />
  <meta name="twitter:description" content="{meta['meta_desc']}" />
  <meta name="twitter:image" content="{first_img}" />

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&family=Noto+Sans+JP:wght@400;500;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/src/style.css" />

  <!-- Schema.org Article Structured Data -->
  <script type="application/ld+json">
  {json.dumps(json_ld_article, ensure_ascii=False, indent=2)}
  </script>

  <!-- Schema.org BreadcrumbList Structured Data -->
  <script type="application/ld+json">
  {json.dumps(json_ld_breadcrumb, ensure_ascii=False, indent=2)}
  </script>

  <!-- Schema.org FAQPage Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": {json.dumps(faq_schema_list, ensure_ascii=False, indent=4)}
  }}
  </script>

  <style>
  {ADVANCED_CSS}
  </style>
</head>
<body>

  <!-- Sticky Minimal Header -->
  <header class="site-header">
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
        <a href="/#catalog" class="nav-link"><span>小型家電カタログ</span></a>
      </nav>
    </div>
  </header>

  <article class="article-container">
    <!-- Breadcrumb Navigation -->
    <nav class="breadcrumb-nav" aria-label="パンくずリスト">
      <a href="/">ホーム</a>
      <span class="breadcrumb-separator">›</span>
      <a href="/#editorial">特集コラム</a>
      <span class="breadcrumb-separator">›</span>
      <span>{meta['breadcrumb_name']}</span>
    </nav>

    <header class="article-header">
      <span class="article-tag">🔥 2026年最新 暖房＆快眠小型家電特集</span>
      <h1 class="article-h1">{meta['h1']}</h1>
      <div class="article-meta">
        <span>📅 最終更新日: 2026.11.12</span>
        <span>✍️ 執筆・監修: クラカジ家電検証チーム</span>
        <span>⏱ 読了目安: 7分</span>
      </div>
      <p class="article-lead">
        {meta['meta_desc']}
        <br /><br />
        急な冷え込みや電気代高騰に備えて、後悔しないベストな1台を見つける完全ガイドとしてご活用ください。
      </p>
    </header>

    <!-- Buying Guide & Comparison Table -->
    {meta['guide_section']}

    <!-- Table of Contents -->
    <nav class="toc-box" aria-label="目次">
      <div class="toc-title">📑 ランキング目次（クリックでジャンプ）</div>
      <ul class="toc-list">
'''
    for it in items:
        html += f'''        <li><a href="#rank-{it['rank']}">第{it['rank']}位：{it['name']}（参考価格：{it['price']}）</a></li>\n'''

    html += '''      </ul>
    </nav>

    <!-- Product Rankings Section -->
    <div class="rankings-wrap">
'''

    for idx, it in enumerate(items):
        exp = expansions[idx % len(expansions)]
        badge_cls = 'top1' if it['rank'] == 1 else ('top2' if it['rank'] == 2 else ('top3' if it['rank'] == 3 else ''))
        badge_label = 'BEST BUY #1 (最優秀大賞)' if it['rank'] == 1 else (f'TOP #{it["rank"]} 厳選' if it['rank'] <= 3 else f'RANK #{it["rank"]}')

        gallery_html = ''
        for img_url in it['images'][:3]:
            gallery_html += f'<img src="{img_url}" alt="{it["name"]}" loading="lazy" />\n'

        pros_html = ''.join([f'<li>{p}</li>' for p in exp['pros']])
        cons_html = ''.join([f'<li>{c}</li>' for c in exp['cons']])

        html += f'''
      <section class="rank-card" id="rank-{it['rank']}">
        <div class="rank-badge-wrap">
          <div class="rank-badge {badge_cls}">#{it['rank']}</div>
          <span class="rank-badge-label">{badge_label}</span>
        </div>
        <h2 class="rank-item-title">第{it['rank']}位：{it['name']}</h2>

        <!-- Gallery of 1-3 images directly from Rakuten CDN -->
        <div class="rank-gallery">
          {gallery_html}
        </div>

        <!-- Deep Review & Verification -->
        <div class="deep-review-box">
          <h4>🧪 プロによる実機検証＆おすすめポイント</h4>
          <p>{exp['review']}</p>
        </div>

        <!-- Pros and Cons Grid -->
        <div class="pros-cons-grid">
          <div class="pros-box">
            <h5>👍 ここが優れている点（メリット）</h5>
            <ul>
              {pros_html}
            </ul>
          </div>

          <div class="cons-box">
            <h5>⚠️ 購入前に確認したい注意点（デメリット）</h5>
            <ul>
              {cons_html}
            </ul>
          </div>
        </div>

        <!-- Specifications & Electricity -->
        <ul class="specs-list">
          <li>・<strong>電気代の目安</strong>: {exp['electricity']}</li>
          <li>・<strong>公式・認証</strong>: 国内PSEマーク・安全基準準拠</li>
        </ul>

        <!-- Real User Voice -->
        <div class="user-voice-box">
          <strong>💬 実際の購入ユーザーの口コミ・声:</strong><br />
          {exp['user_voice']}
        </div>

        <!-- CTA Row -->
        <div class="rank-cta-row">
          <div>
            <span style="font-size: 0.75rem; color: var(--color-text-muted); display: block;">楽天市場 参考価格（税込）</span>
            <span class="rank-price">{it['price']}</span>
          </div>
          <a href="{it['url']}" target="_blank" rel="noopener noreferrer nofollow" class="rank-cta-btn">
            楽天市場で最安値・在庫を見る <span>→</span>
          </a>
        </div>
      </section>
'''

    html += f'''
    </div>

    <!-- FAQ Accordion Section -->
    <section class="faq-box">
      <h2>❓ よくある質問（FAQ）</h2>
'''
    for f in meta['faq']:
        html += f'''
      <div class="faq-item">
        <div class="faq-q"><span>Q.</span> {f['q']}</div>
        <div class="faq-a">{f['a']}</div>
      </div>
'''

    html += f'''
    </section>

    <!-- Bottom Related Articles & CTA -->
    <div style="background: #ffffff; padding: 2.25rem; border-radius: var(--radius-lg); border: 1.5px solid var(--color-border); text-align: center; margin-top: 3.5rem; box-shadow: var(--shadow-sm);">
      <h3 style="font-size: 1.3rem; font-weight: 800; margin-bottom: 0.75rem;">2026年冬の暖房・生活改善を完璧にする関連特集</h3>
      <p style="font-size: 0.92rem; color: var(--color-text-muted); max-width: 580px; margin: 0 auto 1.5rem; line-height: 1.7;">
        用途やスペースに合わせて小型暖房家電を使い分けることで、真冬の快適さと大幅な電気代削減を両立できます。
      </p>
      <div style="display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap;">
        <a href="/articles/large-room-heater-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">広い部屋用暖房TOP10</a>
        <a href="/articles/single-person-kotatsu-heater-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">一人用こたつTOP10</a>
        <a href="/articles/wearable-blanket-rechargeable-warmer-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">電気着る毛布TOP10</a>
        <a href="/articles/desk-panel-heater-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">デスクパネルヒーターTOP10</a>
        <a href="/articles/compact-futon-dryer-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">コンパクト布団乾燥機TOP10</a>
      </div>
      <div style="margin-top: 1.75rem;">
        <a href="/" style="display: inline-block; padding: 0.8rem 2rem; background: var(--color-brand-primary); color: #fff; border-radius: var(--radius-full); font-weight: 800; font-size: 0.95rem; text-decoration: none;">
          クラカジの小型家電カタログトップへ
        </a>
      </div>
    </div>

  </article>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand-note">
        <strong style="color: var(--color-text-main); font-size: 1.05rem;">クラカジ</strong>
        <p style="margin-top: 0.4rem; color: var(--color-text-muted);">
          暮らしをスマートにする小型家電・生活雑貨家電のセレクトカタログメディア。<br />
          ※当サイトはアフィリエイト広告を利用して商品をご紹介しています。
        </p>
      </div>
      <nav class="footer-nav" aria-label="フッターリンク">
        <a href="/">ホーム</a>
        <a href="/#catalog">商品一覧</a>
        <a href="/#editorial">特集コラム</a>
      </nav>
      <div class="copyright">
        &copy; 2026 クラカジ (Kurakaji) All Rights Reserved.
      </div>
    </div>
  </footer>

</body>
</html>
'''

    with open(filepath, 'w', encoding='utf-8') as out_f:
        out_f.write(html)
    print(f'Successfully built Super-SEO Article: {filepath}')

print('Both new articles built successfully!')
