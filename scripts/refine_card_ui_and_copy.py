import re

# 1. Update src/data.js with concise 1-line punchy catchphrases (<= 28 chars, never truncated)
with open('src/data.js', 'r', encoding='utf-8') as f:
    data_content = f.read()

# Let's replace taglines in INITIAL_ITEMS with short, impactful 1-line copy
tagline_replacements = {
    "コードレスで場所を選ばず使える静音DCサーキュレーター。3D立体首振りと長時間バッテリー駆動で一年中大活躍。": "部屋干し3倍速！コードレス静音DC",
    "超音波微粒子ミストでデスク周りを潤す小型加湿器。七色イルミネーションと次亜塩素酸水対応で安心。": "乾燥撃退！卓上静音USB加湿器",
    "超音波の微細振動でメガネや時計の皮脂汚れ・汗を強力洗浄。水だけで隙間の汚れをごっそり落とす。": "メガネ皮脂汚れ落とし！超音波洗浄",
    "1℃刻みの温度調節と保温機能を備えたスリム電気ケトル。細口ノズルでドリップコーヒーにも最適。": "1℃刻み温度調節！朝1分速沸ケトル",
    "A4サイズに収まるコンパクトな卓上ホットプレート。深鍋・たこ焼き対応で一人暮らしの自炊が楽しくなる。": "A4極小サイズ！煮る焼く卓上小鍋",
    "USB充電式でどこでも使える超強力毛玉取り器。ニットや靴下をおろしたての新品の風合いに。": "服が新品に復活！6枚刃電動毛玉取り",
    "パワフルな吸引力とスタイリッシュな軽量ボディ。車内やデスクのちょっとしたゴミを秒速で吸い取る。": "500g超軽量！机と車内の一撃掃除",
    "マット不要でホースを差し込むだけの速暖布団乾燥機。冷えた布団をわずか20分で極上の温もりに。": "冷えた布団が20分で極楽！速暖乾燥",
    "0.5〜1.5合を最短14分で炊き上げる極小炊飯器。冷凍ご飯いらずで毎日炊きたてのおいしさを。": "最短14分炊飯！茶碗1杯の極上自炊",
    "ハンガーにかけたまま素早くシワ伸ばし＆脱臭ができる軽量スチーマー。立ち上がり20秒で朝の救世主に。": "立ち上がり20秒！台不要シワ伸ばし",
    "コンパクトながらHEPAフィルターを搭載した実力派空気清浄機。花粉やハウスダストを逃さずキャッチ。": "花粉ハウスダスト撃退！卓上清浄機",
    "遠赤外線で足元をじんわり包み込む折りたたみパネルヒーター。無音・無風でオフィスの冷えを完全ブロック。": "1時間4円！デスク足元ポカポカ暖房"
}

for old_tag, new_tag in tagline_replacements.items():
    data_content = data_content.replace(old_tag, new_tag)

with open('src/data.js', 'w', encoding='utf-8') as f:
    f.write(data_content)
print("src/data.js updated with punchy 1-line catchphrases!")

# 2. Update src/main.js:
# - Fix tagline generation in fetchProducts fallback
# - Structure card-footer into distinct 3 vertical rows:
#   Row 1: Shop Name
#   Row 2: Reference Price
#   Row 3: Full-width CTA button
with open('src/main.js', 'r', encoding='utf-8') as f:
    main_content = f.read()

# Replace card-footer template
old_footer = '''        <div class="card-footer">
          <div class="price-block">
            <span class="price-label">参考価格 (${item.shopName || '楽天市場'})</span>
            <span class="price-num">${item.priceFormatted || Number(item.price).toLocaleString() + '円'}</span>
          </div>
          <a 
            href="${item.affiliateUrl}" 
            target="_blank" 
            rel="noopener noreferrer nofollow" 
            class="card-cta-btn"
          >
            楽天市場で見る <span>→</span>
          </a>
        </div>'''

new_footer = '''        <div class="card-footer">
          <div class="shop-name-row">
            <span class="shop-badge">取扱店</span>
            <span class="shop-title" title="${item.shopName || '楽天市場'}">${item.shopName || '楽天市場'}</span>
          </div>
          <div class="price-row">
            <span class="price-label">参考価格（税込）</span>
            <span class="price-num">${item.priceFormatted || Number(item.price).toLocaleString() + '円'}</span>
          </div>
          <a 
            href="${item.affiliateUrl}" 
            target="_blank" 
            rel="noopener noreferrer nofollow" 
            class="card-cta-btn"
          >
            楽天市場で詳細・在庫を見る <span>→</span>
          </a>
        </div>'''

if old_footer in main_content:
    main_content = main_content.replace(old_footer, new_footer)
    with open('src/main.js', 'w', encoding='utf-8') as f:
        f.write(main_content)
    print("src/main.js card-footer replaced with clean 3-row layout!")
else:
    print("Warning: old_footer pattern not found in src/main.js")

