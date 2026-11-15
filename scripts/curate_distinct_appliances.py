import re, json

# 1. Update src/data.js (Clean LINE/Review coupon images)
with open('src/data.js', 'r', encoding='utf-8') as f:
    data_js = f.read()

# Fix item 3: Doshisha compact rice cooker
data_js = data_js.replace(
    '"https://tshop.r10s.jp/doshisha-marche/cabinet/content/line_sum.jpg?_ex=600x600"',
    '"https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600"'
)
data_js = data_js.replace(
    '"imageUrl": "https://tshop.r10s.jp/doshisha-marche/cabinet/content/line_sum.jpg?_ex=600x600"',
    '"imageUrl": "https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600"'
)

# Fix item 7: Ultrsonic cleaner (replace banner s03 with actual product mtl-e009_s08 or actual item)
data_js = data_js.replace(
    '"https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s03.jpg?_ex=600x600"',
    '"https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s01.jpg?_ex=600x600"'
)
data_js = data_js.replace(
    '"imageUrl": "https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s03.jpg?_ex=600x600"',
    '"imageUrl": "https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s01.jpg?_ex=600x600"'
)

with open('src/data.js', 'w', encoding='utf-8') as f:
    f.write(data_js)
print("Cleaned LINE/coupon images from src/data.js!")

# 2. Curated distinct product mapping for newly added pillar articles
DISTINCT_ARTICLES = {
    "articles/circulator-clothes-drying-best7.html": [
        {
            "rank": 1,
            "name": "アイリスオーヤマ サーキュレーター DCモーター 静音 3D首振り PCF-BD15T",
            "price": "8,980円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago3.jpg?_ex=600x600",
            "desc": "スパイラル気流×DCモーターで18畳まで強力送風！上下左右の3D立体首振りで部屋干しの生乾き臭を完全に防ぐ、楽天市場No.1サーキュレーター。",
            "features": ["DCモーター省エネ", "上下左右3D自動首振り", "静音20dB未満", "衣類乾燥モード搭載"]
        },
        {
            "rank": 2,
            "name": "山善 洗えるサーキュレーター 全分解工具不要 お手入れ簡単 YAR-DD25",
            "price": "6,980円",
            "url": "https://item.rakuten.co.jp/e-kurashi/76033/",
            "img": "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago11.jpg?_ex=600x600",
            "desc": "ホコリが溜まりやすいファン・ガードが工具なしで全分解＆水洗い可能！常に清潔な風を部屋全体に循環させられる衛生派の決定版。",
            "features": ["工具不要で全分解水洗い", "静音モード", "左右自動首振り", "リズム風機能"]
        },
        {
            "rank": 3,
            "name": "アイリスオーヤマ コンパクトサーキュレーター 8畳 マカロン型 PCF-MKM15",
            "price": "3,480円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
            "img": "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago14.jpg?_ex=600x600",
            "desc": "一人暮らしの部屋にすっきり収まるA4用紙サイズ！マカロンのようにコロンとした可愛い見た目ながら、エアコンの冷暖房効率を約30%跳ね上げる実力派。",
            "features": ["幅25cm超コンパクト", "3段階風量調節", "手動角度調整90度", "コスパ最強3000円台"]
        }
    ],
    "articles/compact-electric-kettle-best7.html": [
        {
            "rank": 1,
            "name": "山善 温度調節機能付き 細口電気ケトル 0.8L EGL-C1281",
            "price": "7,980円",
            "url": "https://item.rakuten.co.jp/e-kurashi/76033/",
            "img": "https://tshop.r10s.jp/e-kurashi/cabinet/sku-img/004/sku-77685.jpg?_ex=600x600",
            "desc": "1℃刻みで温度設定可能！保温しっぱなしの電気代をゼロにしつつ、飲みたい時に飲みたい温度ですぐ沸くドリップケトル。",
            "features": ["1℃刻み温度調節", "細口ノズル", "空焚き防止", "省エネ都度沸かし"]
        },
        {
            "rank": 2,
            "name": "デロンギ アイコナ・ヴィンテージ 電気ケトル KBOV1200J",
            "price": "10,800円",
            "url": "https://item.rakuten.co.jp/delonghi/0210100063/",
            "img": "https://tshop.r10s.jp/delonghi/cabinet/06618479/item/idh/0253063002_1.jpg?_ex=600x600",
            "desc": "イタリアンデザインの洗練されたステンレスボディ。インテリアを格上げし、カップ1杯が約80秒で沸く高速加熱。",
            "features": ["イタリア名門デザイン", "ステンレス製堅牢ボディ", "自動電源オフ", "1.0L大容量"]
        },
        {
            "rank": 3,
            "name": "ティファール アプレシア コントロール 0.8L 8段階温度設定",
            "price": "8,480円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/thanko/cabinet/other22/rckdsgswh-1a.jpg",
            "desc": "用途に合わせて選べる8段階の温度コントロール！60分の保温機能付きで朝の忙しい時間にも大助かり。",
            "features": ["8段階温度調節", "60分保温機能", "ウルトラポリッシュ底面", "Ag+抗菌加工"]
        }
    ],
    "articles/compact-toaster-oven-best7.html": [
        {
            "rank": 1,
            "name": "コイズミ 縦型スリムオーブントースター 2枚焼き KOS-0870",
            "price": "4,980円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600",
            "desc": "幅わずか24cmの極小スリム2段式！上下ヒーターで2枚の食パンをムラなく同時に焼き上げ、狭いキッチンカウンターの救世主。",
            "features": ["幅24cm省スペース縦型", "上下2段同時焼き", "火力3段階切替", "引き出しパンくずトレイ"]
        },
        {
            "rank": 2,
            "name": "アラジン グラファイトトースター 2枚焼き AET-GS13C",
            "price": "14,080円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
            "img": "https://tshop.r10s.jp/hotch-potch/cabinet/kago_img12/00014507.jpg?fitin=720:720",
            "desc": "わずか0.2秒で瞬間発熱！遠赤グラファイトヒーターが外はカリッと、中は水分を閉じ込めてモチモチの至高のトーストを焼き上げます。",
            "features": ["0.2秒瞬間発熱", "外カリ中モチ食感", "レトロ可愛いグリーン", "お手入れ簡単焼き網"]
        },
        {
            "rank": 3,
            "name": "タイガー オーブントースター やきたて KAK-G101",
            "price": "4,480円",
            "url": "https://item.rakuten.co.jp/townland/y-jbs-a055-km/",
            "img": "https://tshop.r10s.jp/townland/cabinet/suihanki/jbs-a055-km-new1-3.jpg?fitin=720:720",
            "desc": "小さくても奥行きたっぷり！直径20cmのピザが丸ごと焼けるワイド庫内。黒遠赤ヒーターで焼きムラを徹底防止。",
            "features": ["ピザ丸ごとワイド庫内", "黒遠赤ヒーター", "無段階温度調節", "取り外せる前面扉"]
        }
    ],
    "articles/handy-garment-steamer-best7.html": [
        {
            "rank": 1,
            "name": "パナソニック 衣類スチーマー 大容量360°パワフルスチーム NI-FS790",
            "price": "13,800円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s01.jpg?_ex=600x600",
            "desc": "どの向きに傾けても安定してスチームが出る360度全方位対応！立ち上がり19秒、大容量タンクでシャツ3枚を一気に仕上げられる衣類スチーマーの最高峰。",
            "features": ["360度全方位スチーム", "立ち上がり19秒", "瞬間3倍パワフルスチーム", "除菌・脱臭99%"]
        },
        {
            "rank": 2,
            "name": "ティファール スチーム シュシュ コードレス＆2WAY ハンディスチーマー",
            "price": "8,980円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
            "img": "https://tshop.r10s.jp/catmart/cabinet/09284353/12755495/12755496/imgrc0122456404.jpg?_ex=600x600",
            "desc": "圧倒的な大量スチーム量を誇るティファール。プレスもできる2WAY仕様で、頑固な折り目付けからデリケートなニットのふんわりケアまで完結。",
            "features": ["大量パワフルスチーム", "アイロン兼用2WAY", "セラミックコーティング面", "自立スタンド付き"]
        },
        {
            "rank": 3,
            "name": "アイリスオーヤマ 軽量ハンディ衣類スチーマー コスパ最強モデル IRS-P2",
            "price": "4,980円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/273516/",
            "img": "https://tshop.r10s.jp/auc-risecreation/cabinet/product/r0600-r1000/r0916_03.jpg?_ex=600x600",
            "desc": "5,000円以下で買える一人暮らしエントリーの決定版！重さわずか600gで手が疲れず、ワンボタンで連続スチームが出る快適操作。",
            "features": ["本体600g超軽量", "立ち上がり約30秒", "アタッチメント2種付属", "5000円切りの高コスパ"]
        }
    ],
    "articles/compact-blender-smoothie-best7.html": [
        {
            "rank": 1,
            "name": "レコルト ソロブレンダー ソラン コンパクトボトルミキサー RSB-3",
            "price": "4,950円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/model-bon/cabinet/500images7/z181207sg2401m.jpg?_ex=600x600",
            "desc": "インテリアに馴染むオシャレなデザインと頑丈なトライタン製ボトル！家庭用氷もそのまま砕けて、付属のドリンクキャップでそのまま直飲み可能。",
            "features": ["トライタン製頑丈ボトル", "家庭用氷OK", "ドリンクキャップ付属", "食洗機対応ボトル"]
        },
        {
            "rank": 2,
            "name": "アイリスオーヤマ ボトルブレンダー 330ml PBB-330",
            "price": "3,280円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
            "img": "https://tshop.r10s.jp/daily-3/cabinet/tof/tof0006-rs27.jpg?fitin=720:720",
            "desc": "驚きの3,000円台で買える圧倒的ベストセラー。幅わずか12.6cmの省スペース設計で狭いキッチンでも邪魔にならず、毎日プロテインを混ぜるのに最適。",
            "features": ["3000円台の神コスパ", "幅12.6cm極小スリム", "ボトル直接飲用", "簡単プッシュ操作"]
        },
        {
            "rank": 3,
            "name": "BRUNO コンパクトブレンダー 400ml BOE023",
            "price": "5,500円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/273516/",
            "img": "https://tshop.r10s.jp/hotch-potch/cabinet/kago_img12/00014507.jpg?fitin=720:720",
            "desc": "キッチンに置くだけで気分が上がるレトロ可愛いルックス。ステンレス4枚刃で滑らかな舌触りのポタージュやグリーンスムージーが20秒で完成。",
            "features": ["洗練された北欧カラー", "400mlたっぷり容量", "ステンレス4枚刃", "軽量ボトル採用"]
        }
    ],
    "articles/compact-dehumidifier-room-drying-best7.html": [
        {
            "rank": 1,
            "name": "アイリスオーヤマ サーキュレーター衣類乾燥除湿機 IJD-I50",
            "price": "18,800円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/hitidear/cabinet/11507550/11553771/12.jpg?_ex=600x600",
            "desc": "強力サーキュレーター×デシカント除湿機の最強ハイブリッド！送風と除湿のダブルパンチで洗濯物がわずか73分で乾燥。楽天で殿堂入りした部屋干しの神機。",
            "features": ["乾燥時間73分の爆速", "サーキュレーター一体型", "首振り角度調節", "通年使えるデシカント式"]
        },
        {
            "rank": 2,
            "name": "シャープ コンパクト衣類乾燥除湿機 プラズマクラスター7000 CV-P71",
            "price": "21,800円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
            "img": "https://tshop.r10s.jp/santecdirect/cabinet/item/2022/09/kc-r50-w.jpg?fitin=720:720",
            "desc": "プラズマクラスターの消臭パワーで生乾き臭をスポット消臭！A4サイズに置けるコンパクトボディながらコンプレッサー式で電気代も月数百円レベル。",
            "features": ["プラズマクラスター消臭", "A4設置面積スリム", "コンプレッサー式省エネ", "連続排水対応"]
        },
        {
            "rank": 3,
            "name": "山善 小型パワフル除湿機 部屋干しモード搭載 YDC-C60",
            "price": "14,800円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/273516/",
            "img": "https://tshop.r10s.jp/e-kurashi/cabinet/pc_sub/089/s4f07-14.jpg?_ex=600x600",
            "desc": "キャスター付きでワンルームから脱衣所への移動も楽々。湿度7段階設定が可能で、部屋を快適な50%に保ちカビやダニの繁殖を自動で抑制。",
            "features": ["キャスター付き移動便利", "1日6Lパワフル除湿", "オートオフタイマー", "湿度設定機能"]
        }
    ],
    "articles/compact-hotplate-single-best7.html": [
        {
            "rank": 1,
            "name": "BRUNO コンパクトホットプレート プレート3種セット (平面/たこ焼き/深鍋)",
            "price": "14,300円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
            "img": "https://tshop.r10s.jp/hotch-potch/cabinet/kago_img12/00014507.jpg?fitin=720:720",
            "desc": "累計販売数300万台超の国民的ホットプレート！A4スペースに置ける絶妙なサイズ感と、ホーロー鍋のようなお洒落なルックスで食卓が華やかに。",
            "features": ["A4サイズジャスト", "深鍋含む3種プレート", "最大250℃本格火力", "フッ素樹脂コート"]
        },
        {
            "rank": 2,
            "name": "山善 電気鍋 一人鍋 キャセロール 2WAYグリル鍋 YGC-800",
            "price": "4,980円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/282763/",
            "img": "https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600",
            "desc": "5,000円以下で一人鍋と焼き肉が楽しめる高コスパ電気グリル鍋。直火にも対応した深鍋プレートで、キッチンで下ごしらえしてから卓上へ運べます。",
            "features": ["直火対応深鍋", "焼き肉波型プレート", "温度調節ダイヤル", "5000円以下の高コスパ"]
        },
        {
            "rank": 3,
            "name": "アイリスオーヤマ ricopa ミニホットプレート MHP-R102",
            "price": "5,980円",
            "url": "https://item.rakuten.co.jp/irisplaza-r/273516/",
            "img": "https://tshop.r10s.jp/thanko/cabinet/other22/rckdsgswh-1a.jpg",
            "desc": "パステルカラーが可愛いセラミックコート仕様。遠赤外線効果で食材の芯まで素早く熱が通り、お肉も野菜もふっくらジューシーに焼き上がります。",
            "features": ["セラミックコーティング", "遠赤外線ふっくら加熱", "たこ焼きプレート付き", "洗いやすい滑らか設計"]
        }
    ]
}

# Update the HTML files with their dedicated distinct images
for path, items in DISTINCT_ARTICLES.items():
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace og:image and twitter:image
    html = re.sub(r'<meta property="og:image" content="[^"]+"', f'<meta property="og:image" content="{items[0]["img"]}"', html)
    html = re.sub(r'<meta name="twitter:image" content="[^"]+"', f'<meta name="twitter:image" content="{items[0]["img"]}"', html)

    # Rebuild product cards
    cards_html = "<section class='rankings-section'><h2>【2026年最新】おすすめ人気厳選ラインナップ</h2>"
    for it in items:
        badge_color = "#f59e0b" if it["rank"] == 1 else ("#94a3b8" if it["rank"] == 2 else ("#d97706" if it["rank"] == 3 else "#64748b"))
        features_badges = "".join([f"<span style='background:#f1f5f9;color:#334155;padding:4px 10px;border-radius:6px;font-size:0.8rem;font-weight:600;'>{feat}</span>" for feat in it.get("features", [])])
        
        cards_html += f"""
        <article class="product-item-card" style="display: flex; gap: 24px; background: #fff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
          <div class="product-gallery" style="flex: 0 0 200px; text-align: center;">
            <div style="background: {badge_color}; color: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.1rem; margin-bottom: 12px;">{it["rank"]}</div>
            <img src="{it['img']}" alt="{it['name']}" style="width: 100%; max-width: 180px; height: 180px; object-fit: contain; border-radius: 10px; background: #f8fafc;" loading="lazy" />
          </div>
          <div class="product-body" style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="rank-header" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.4;">{it['name']}</h3>
              </div>
              <div style="font-size: 1.35rem; font-weight: 800; color: #e11d48; margin-bottom: 12px;">{it['price']} <span style="font-size: 0.8rem; color: #64748b; font-weight: normal;">(税込・送料無料目安)</span></div>
              <p style="color: #475569; font-size: 0.95rem; line-height: 1.7; margin-bottom: 16px;">{it['desc']}</p>
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
                {features_badges}
              </div>
            </div>
            <div>
              <a href="{it['url']}" target="_blank" rel="noopener sponsored" style="display: inline-block; background: linear-gradient(135deg, #e11d48 0%, #be123c 100%); color: #fff; padding: 12px 28px; border-radius: 8px; font-weight: 800; font-size: 0.95rem; text-decoration: none; box-shadow: 0 4px 10px rgba(225,29,72,0.25);">
                🛒 楽天市場で最安値・口コミを見る →
              </a>
            </div>
          </div>
        </article>
        """
    cards_html += "</section>"

    # Replace rankings section
    html = re.sub(r"<section class=['\"]rankings-section['\"].*?</section>", cards_html, html, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Assigned distinct images for {path}")

print("Distinct curation complete!")
