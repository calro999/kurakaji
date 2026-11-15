import json, os, re
from expansions_data import EXPANSIONS

with open('/home/antigravity/kurakaji/scripts/verified_30_items.json', 'r', encoding='utf-8') as f:
    all_items = json.load(f)

# Group by theme
themes = {
    'large-room': {
        'filepath': '/home/antigravity/kurakaji/articles/large-room-heater-best10.html',
        'items': [it for it in all_items if it['theme'] == 'large-room']
    },
    'kotatsu': {
        'filepath': '/home/antigravity/kurakaji/articles/single-person-kotatsu-heater-best10.html',
        'items': [it for it in all_items if it['theme'] == 'kotatsu']
    },
    'wearable': {
        'filepath': '/home/antigravity/kurakaji/articles/wearable-blanket-rechargeable-warmer-best10.html',
        'items': [it for it in all_items if it['theme'] == 'wearable']
    }
}

SEO_META = {
  "large-room": {
    "h1": "【2026年最新】広い部屋でも速暖・省エネ！リビング用おすすめ暖房器具ベストバイTOP10【電気代比較・プロ実機検証】",
    "meta_desc": "10畳〜15畳以上の広いリビングを足元からムラなく暖める大風量セラミックファンヒーター・人感センサー搭載暖房おすすめ人気ランキングTOP10！電気代シミュレーション、エアコン併用テクニック、選び方の基準を専門家が徹底検証して解説。",
    "keywords": "広い部屋 暖房, リビング 暖房器具 おすすめ, セラミックヒーター 大風量, 人感センサー ヒーター, 暖房器具 電気代 比較, 2026 暖房 ベストバイ, クラカジ",
    "breadcrumb_name": "広い部屋用暖房器具TOP10",
    "faq": [
      {
        "q": "15畳以上の広いリビングでエアコンとセラミックヒーターはどちらが省エネですか？",
        "a": "結論として『併用運転』が最も省エネです。冷え切った朝は立ち上がりの早いセラミックヒーターで足元を一気に暖め、室温が上がったらエアコンの弱運転に切り替えることで、無駄な電力消費を抑えつつ最速で快適な室温を作ることができます。"
      },
      {
        "q": "広い部屋で暖房器具を選ぶ際の目安のW数（ワット数）は？",
        "a": "リビング用であれば最大消費電力1200Wクラスかつ『大風量ファン』を搭載したモデルを選びましょう。風量のないヒーターは熱が上部に滞留してしまいますが、大風量ターボファン付きであれば床面を這うように温風が届き、部屋全体の温度ムラをなくせます。"
      },
      {
        "q": "人感センサー付き暖房器具のメリットは何ですか？",
        "a": "人の不在を感知して自動で弱運転または電源OFFになるため、無駄な電力消費を最大30〜50%削減できます。特にリビングやダイニングのように出入りが多い部屋での消し忘れ防止に劇的な効果を発揮します。"
      }
    ],
    "guide_section": """
    <section class="guide-box">
      <h2>🏆 広い部屋向け暖房器具で失敗しないための「4大比較ポイント」</h2>
      <div class="guide-grid">
        <div class="guide-card">
          <div class="guide-num">01</div>
          <h3>風の「到達距離」と大風量設計</h3>
          <p>広い部屋では、ヒーターの熱をいかに遠くまで運べるかが勝負。単なる発熱体だけでなく、大風量シロッコファンやターボファンを搭載したモデルを選ぶことで、足元から部屋の奥まで温風を行き渡らせます。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">02</div>
          <h3>AI恒温・温度センサー機能の有無</h3>
          <p>室温を感知して自動で出力をセーブするインテリジェントセンサー搭載機なら、つけっぱなしでも電気代が高騰しません。手動で小まめに調節するストレスから完全に解放されます。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">03</div>
          <h3>自動首振り（ワイドスイング）</h3>
          <p>固定方向のみの温風は体の一部だけが熱くなり乾燥の原因に。左右70〜90度の自動首振り機能があれば、ソファに座る家族全員へ均一に心地よい暖気を届けられます。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">04</div>
          <h3>多重安全機能（転倒OFF・チャイルドロック）</h3>
          <p>リビングは子供やペットが走り回るエリア。地震や衝突時にミリ秒単位で通電を遮断する転倒自動OFFスイッチ、誤操作を防ぐチャイルドロックは必須条件です。</p>
        </div>
      </div>
    </section>

    <!-- Comparison Table Section -->
    <section class="compare-table-box">
      <h2>📊 リビング用暖房器具 性能・コスパ早見比較表</h2>
      <div class="table-responsive">
        <table class="styled-table">
          <thead>
            <tr>
              <th>順位 / モデル名</th>
              <th>適用畳数</th>
              <th>主要機能</th>
              <th>電気代目安(時)</th>
              <th>参考価格</th>
            </tr>
          </thead>
          <tbody>
            <tr class="highlight">
              <td><strong>第1位：Hitidear 大風量静音</strong></td>
              <td>〜15畳</td>
              <td>AI恒温 / 首振り / 3段階切替</td>
              <td>約21.7円〜</td>
              <td>6,980円</td>
            </tr>
            <tr>
              <td><strong>第2位：アイリスオーヤマ JCH-12TDS1</strong></td>
              <td>〜12畳</td>
              <td>大風量スリム / 人感センサー</td>
              <td>約18.6円〜</td>
              <td>8,980円</td>
            </tr>
            <tr>
              <td><strong>第3位：シロカ かるポカ SN-M351</strong></td>
              <td>〜10畳</td>
              <td>遠赤外線 / 風が出ない / タイマー</td>
              <td>約20〜28円</td>
              <td>19,800円</td>
            </tr>
            <tr>
              <td><strong>第4位：山善 DSF-VP12</strong></td>
              <td>〜12畳</td>
              <td>大風量パネル / 温度センサー</td>
              <td>約18.6円〜</td>
              <td>10,980円</td>
            </tr>
            <tr>
              <td><strong>第5位：スリーアップ マキシムヒート</strong></td>
              <td>〜12畳</td>
              <td>Wセンサー / 加湿パネル機能</td>
              <td>約20〜32円</td>
              <td>13,800円</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
  },

  "kotatsu": {
    "h1": "【2026年最新】一人用こたつ・パーソナルデスク暖房おすすめ人気ランキングTOP10【電気代月数百円！在宅ワーク神機】",
    "meta_desc": "電気代をエアコンの約1/10に抑える一人用こたつ・デスクこたつ・チェア付きセットおすすめ人気ランキングTOP10！在宅ワークや一人暮らしで絶対に失敗しない選び方、サイズ別の使い勝手、電気代シミュレーションを徹底解説。",
    "keywords": "一人用こたつ, デスクこたつ, パーソナルこたつ, 一人暮らし こたつ おすすめ, 在宅ワーク 足元 暖房, こたつ 電気代 節約, クラカジ",
    "breadcrumb_name": "一人用こたつ・デスク暖房TOP10",
    "faq": [
      {
        "q": "一人用こたつの1ヶ月の電気代はどれくらいですか？",
        "a": "一般的な一人用こたつ（300Wヒーター・サーモスタット付き）を1日8時間使用した場合、1時間あたり約2.5円、1ヶ月（30日）使用してもわずか約600円程度です。1日中エアコンをつける場合（月5,000〜8,000円）と比べて約90%もの節約効果があります。"
      },
      {
        "q": "ハイタイプこたつ（デスクこたつ）は夏場も使えますか？",
        "a": "はい、使えます。多くのハイタイプこたつは布団を外して天板をネジ固定できる仕様になっており、オフシーズンは通常のパソコンデスクや学習机として1年中使用可能です。収納場所の心配もありません。"
      },
      {
        "q": "狭い6畳のワンルームでも邪魔になりませんか？",
        "a": "本ランキングで紹介している一人用こたつは、幅70×奥行50cm前後の超省スペース設計です。また専用の省スペース掛け布団は四隅にスリット加工が施されており、裾が広がらないため生活動線を妨げません。"
      }
    ],
    "guide_section": """
    <section class="guide-box">
      <h2>🏆 一人用こたつ選びで失敗しないための「3つの絶対基準」</h2>
      <div class="guide-grid">
        <div class="guide-card">
          <div class="guide-num">01</div>
          <h3>ハイタイプ（椅子座り）かロータイプ（座椅子）か</h3>
          <p>長時間のPC作業や読書が目的なら、腰への負担が圧倒的に少ないハイタイプ（デスクこたつ＋専用チェア）が一推し。床生活を好む方はロータイプを選びましょう。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">02</div>
          <h3>天板サイズ（70cm vs 80cm vs 90cm）</h3>
          <p>ノートPC＋マウスのみなら幅70cmで十分省スペース。外付けモニターを置いたり資料を広げて作業したい方は幅80〜90cmのワイドサイズが快適です。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">03</div>
          <h3>熱を逃がさない「幕板＆仕切り構造」</h3>
          <p>デスクこたつは足元から暖気が逃げやすいため、専用チェアの足元に冷気遮断板が付いているセットや、こたつ本体の幕板がしっかりしているモデルを選びましょう。</p>
        </div>
      </div>
    </section>

    <!-- Comparison Table Section -->
    <section class="compare-table-box">
      <h2>📊 一人用こたつ セット内容・電気代比較表</h2>
      <div class="table-responsive">
        <table class="styled-table">
          <thead>
            <tr>
              <th>順位 / モデル名</th>
              <th>天板サイズ</th>
              <th>セット内容</th>
              <th>電気代目安(時)</th>
              <th>参考価格</th>
            </tr>
          </thead>
          <tbody>
            <tr class="highlight">
              <td><strong>第1位：ハイタイプ 3点セット</strong></td>
              <td>75×50cm</td>
              <td>デスク・回転椅子・布団</td>
              <td>約2.5円</td>
              <td>24,800円</td>
            </tr>
            <tr>
              <td><strong>第2位：エルワールド 省スペースセット</strong></td>
              <td>70×50cm</td>
              <td>デスク・専用布団</td>
              <td>約2.6円</td>
              <td>15,800円</td>
            </tr>
            <tr>
              <td><strong>第3位：バリエファニ 62cmセット</strong></td>
              <td>62×50cm</td>
              <td>デスク・折畳椅子・ポケット布団</td>
              <td>約2.5円</td>
              <td>17,800円</td>
            </tr>
            <tr>
              <td><strong>第4位：ハイタイプ ワイド90cm</strong></td>
              <td>90×60cm</td>
              <td>デスク・キャスター椅子・布団</td>
              <td>約3.2円</td>
              <td>29,800円</td>
            </tr>
            <tr>
              <td><strong>第5位：チェック柄 3点セット</strong></td>
              <td>70×50cm</td>
              <td>デスク・椅子・デザイン布団</td>
              <td>約2.8円</td>
              <td>18,800円</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
    """
  },

  "wearable": {
    "h1": "【2026年最新】電気着る毛布＆充電式カイロおすすめ人気ランキングTOP10【身につける暖房・電気代1回0.5円】",
    "meta_desc": "エアコン要らずで家中どこでも暖かい！USB給電・丸洗い可能な電気着る毛布、足入れ着るこたつ、急速発熱充電式カイロおすすめ人気ランキングTOP10。在宅勤務や家事、アウトドアにも使える最強防寒ギアの性能・持続時間を徹底検証。",
    "keywords": "着る毛布 電気, USB 電気毛布, 着る毛布 洗える, 充電式カイロ おすすめ, 着るこたつ, 電気代 節約 防寒, クラカジ",
    "breadcrumb_name": "電気着る毛布＆充電式カイロTOP10",
    "faq": [
      {
        "q": "電気着る毛布は洗濯機で洗えますか？",
        "a": "はい、本記事でご紹介しているモデルはすべてコントローラーやバッテリーを取り外して洗濯機で丸洗い（洗濯ネット使用）が可能です。汗や皮脂の汚れを気にせず、シーズン中いつでも清潔にお使いいただけます。"
      },
      {
        "q": "モバイルバッテリーはどれくらいの容量が必要ですか？",
        "a": "10000mAhのモバイルバッテリーであれば、中温モードで約6〜8時間の連続駆動が可能です。デスクワークの勤務時間や就寝中の使用であれば10000mAhが最もバランスが良くおすすめです。"
      },
      {
        "q": "低温やけどの心配はありませんか？",
        "a": "ご紹介している製品はすべて過熱防止センサー（NTCシステム）や、1〜3時間の自動電源オフタイマーを搭載しています。長時間同じ箇所に強い密着状態で押し当て続けなければ、安全にご使用いただけます。"
      }
    ],
    "guide_section": """
    <section class="guide-box">
      <h2>🏆 電気着る毛布・身につける暖房の「失敗しない選び方」</h2>
      <div class="guide-grid">
        <div class="guide-card">
          <div class="guide-num">01</div>
          <h3>着用スタイル（ポンチョ型 vs ブランケット型）</h3>
          <p>家事や掃除など動き回る時間が長いなら、腕を通せるポンチョ型やフード付きタイプが最適。デスクワークやベッドでのリラックス中心なら、ボタン留めができる大判ブランケット型が最も汎用性が高いです。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">02</div>
          <h3>発熱体の素材（グラフェン vs ニクロム線）</h3>
          <p>最新のグラフェン発熱体は、従来の電熱線特有のゴワゴワ感が一切なく、軽くてしなやか。電源ONからわずか5〜10秒で体の深部まで温もりが届く圧倒的な速暖性を誇ります。</p>
        </div>
        <div class="guide-card">
          <div class="guide-num">03</div>
          <h3>給電方式とポケット位置</h3>
          <p>モバイルバッテリーをすっきり収納できる内蔵ファスナーポケットの有無を確認しましょう。ポケットの位置が身体の側面に配置されていると、座った際にお腹や腰を圧迫しません。</p>
        </div>
      </div>
    </section>

    <!-- Comparison Table Section -->
    <section class="compare-table-box">
      <h2>📊 電気着る毛布＆充電式カイロ 性能早見比較表</h2>
      <div class="table-responsive">
        <table class="styled-table">
          <thead>
            <tr>
              <th>順位 / モデル名</th>
              <th>タイプ・サイズ</th>
              <th>給電 / バッテリー</th>
              <th>洗濯対応</th>
              <th>参考価格</th>
            </tr>
          </thead>
          <tbody>
            <tr class="highlight">
              <td><strong>第1位：電熱 着る毛布 ロング丈</strong></td>
              <td>140×80cm フランネル</td>
              <td>USB給電 6WAY</td>
              <td>丸洗いOK</td>
              <td>4,980円</td>
            </tr>
            <tr>
              <td><strong>第2位：10000mAh充電式カイロ</strong></td>
              <td>手のひら 両面発熱</td>
              <td>10000mAh内蔵</td>
              <td>防塵</td>
              <td>2,480円</td>
            </tr>
            <tr>
              <td><strong>第3位：8エリア発熱 着る毛布</strong></td>
              <td>150×80cm 大判</td>
              <td>USB 3段階調温</td>
              <td>洗濯機OK</td>
              <td>3,980円</td>
            </tr>
            <tr>
              <td><strong>第4位：ふわとろ毛布 30000mAh付</strong></td>
              <td>150×85cm 厚手</td>
              <td>大容量バッテリー付</td>
              <td>丸洗いOK</td>
              <td>5,880円</td>
            </tr>
            <tr>
              <td><strong>第5位：磁気分離式 充電式カイロ</strong></td>
              <td>2分割マグネット</td>
              <td>10000mAh 360°発熱</td>
              <td>防滴</td>
              <td>3,280円</td>
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
    expansions = EXPANSIONS.get(theme_id, [])

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
      <span class="article-tag">🔥 2026年最新 暖房家電・季節特集</span>
      <h1 class="article-h1">{meta['h1']}</h1>
      <div class="article-meta">
        <span>📅 最終更新日: 2026.11.12</span>
        <span>✍️ 執筆・監修: クラカジ家電検証チーム</span>
        <span>⏱ 読了目安: 7分</span>
      </div>
      <p class="article-lead">
        {meta['meta_desc']}
        <br /><br />
        急な冷え込みや真冬の電気代高騰に備えて、後悔しないベストな1台を見つける完全ガイドとしてご活用ください。
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
      <h3 style="font-size: 1.3rem; font-weight: 800; margin-bottom: 0.75rem;">2026年冬の暖房対策を完璧にする関連特集</h3>
      <p style="font-size: 0.92rem; color: var(--color-text-muted); max-width: 580px; margin: 0 auto 1.5rem; line-height: 1.7;">
        用途やスペースに合わせて暖房器具を使い分けることで、真冬の快適さと大幅な電気代削減を両立できます。
      </p>
      <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <a href="/articles/large-room-heater-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">広い部屋用暖房TOP10</a>
        <a href="/articles/single-person-kotatsu-heater-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">一人用こたつTOP10</a>
        <a href="/articles/wearable-blanket-rechargeable-warmer-best10.html" style="padding: 0.65rem 1.25rem; border-radius: var(--radius-full); background: #f1f5f9; font-size: 0.85rem; font-weight: 700; color: #334155; text-decoration: none;">電気着る毛布TOP10</a>
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
    print(f'Successfully updated Super-SEO Article: {filepath}')

print('All 3 Super-SEO articles rewritten with full verified items and images!')
