import urllib.request, urllib.parse, json, time, re, html, os

app_id = '4b79f26f-f12a-4720-88b2-c3705cd31fa3'
access_key = 'pk_XWavxZXgqjGudZN5TIIniTSCTQ1vQ7Q14IK1Ce0aJ7Y'
affiliate_id = '54d2a438.4bc4abc2.54d2a439.aa1be583'
api_url = 'https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20260401'

targets = [
    {
        'file': 'articles/circulator-clothes-drying-best7.html',
        'keyword': 'サーキュレーター DCモーター 部屋干し 静音',
        'sub_keyword': 'サーキュレーター DCモーター 3D首振り',
        'genre_tag': 'サーキュレーター',
        'key_feature': '3D立体首振り・DC静音省エネ',
        'merit': '上下左右の強力スパイラル気流で洗濯物を短時間速乾。部屋干し特有の生乾き臭を元から防ぎます。',
        'tags': ['DCモーター省エネ', '上下左右3D立体首振り', '衣類乾燥モード', '静音20dB未満']
    },
    {
        'file': 'articles/compact-blender-smoothie-best7.html',
        'keyword': 'ブレンダー ミキサー ボトル スムージー 小型',
        'sub_keyword': 'ボトルブレンダー コンパクト そのまま飲める',
        'genre_tag': '小型ブレンダー＆ミキサー',
        'key_feature': 'ボトル直飲み・氷対応ハイパワー',
        'merit': '作ったボトルでそのまま持ち運び＆直飲み可能。洗い物が劇的に減り、忙しい朝のスムージー習慣が続きます。',
        'tags': ['そのまま飲めるボトル', '氷粉砕ハイパワー', 'パーツ丸洗い清潔', '省スペース設計']
    },
    {
        'file': 'articles/compact-dehumidifier-room-drying-best7.html',
        'keyword': '除湿機 小型 一人暮らし 部屋干し コンパクト 静音',
        'sub_keyword': '小型除湿機 衣類乾燥 省エネ 一人暮らし',
        'genre_tag': '小型除湿機',
        'key_feature': '小型軽量・部屋干し強力除湿',
        'merit': '狭いワンルームや脱衣所・クローゼットにもすっきり置けるコンパクト設計。湿気・カビ・生乾き臭を徹底ブロック。',
        'tags': ['部屋干し速乾', '静音省エネ設計', '満水自動停止機能', 'カビ・結露防止']
    },
    {
        'file': 'articles/compact-electric-kettle-best7.html',
        'keyword': '電気ケトル 一人暮らし おしゃれ 小型 ドリップ 温度調節',
        'sub_keyword': '電気ケトル 小型 速沸 ドリップポット',
        'genre_tag': '電気ケトル',
        'key_feature': '瞬間沸騰・注ぎやすい極細ノズル',
        'merit': '朝の忙しい時間も1分前後でスピード沸騰。狙った湯量をコントロールできるドリップノズルでコーヒーやスープも格別の味に。',
        'tags': ['スピード沸騰', 'ドリップ用極細ノズル', '空焚き防止機能', '保温・温度調節']
    },
    {
        'file': 'articles/compact-hotplate-single-best7.html',
        'keyword': 'ホットプレート 一人用 小型 鍋 焼肉 卓上',
        'sub_keyword': 'コンパクトホットプレート 一人暮らし ミニ',
        'genre_tag': '小型ホットプレート',
        'key_feature': '1〜2人前ジャストサイズ・着脱式プレート',
        'merit': 'テーブルの上で調理しながら出来立てアツアツを食べられる。一人焼肉から鍋料理・たこ焼きまでマルチに対応。',
        'tags': ['卓上ジャストサイズ', 'プレート丸洗い可能', 'フッ素コート焦げ付き防止', '高火力温度調節']
    },
    {
        'file': 'articles/compact-toaster-oven-best7.html',
        'keyword': 'オーブントースター 縦型 スリム 小型 2枚 省スペース',
        'sub_keyword': 'トースター 縦型 一人暮らし コンパクト',
        'genre_tag': '縦型スリムトースター',
        'key_feature': '縦型2段スリム・高火力均一焼き上げ',
        'merit': '幅をとらない縦型構造で狭いキッチンのわずかな隙間にもピタッと設置可能。外サク中モチの絶品トーストが焼けます。',
        'tags': ['縦型省スペース', '高火力ヒーター', 'パンくずトレイでお手入れ簡単', '火力多段階切替']
    },
    {
        'file': 'articles/electric-lint-remover-best7.html',
        'keyword': '毛玉取り器 電動 充電式 洋服 毛玉クリーナー 強力',
        'sub_keyword': '電動毛玉取り器 コードレス 生地に優しい',
        'genre_tag': '電動毛玉取り器',
        'key_feature': '切れ味抜群ステンレス刃・生地保護ガード',
        'merit': 'ニットやお気に入りのコートをなでるだけで新品のような風合いに復活。生地を傷つけず毛玉だけをごっそりカットします。',
        'tags': ['高精度ステンレス刃', '生地保護ハニカムガード', 'USB充電コードレス', '大容量ダストボックス']
    },
    {
        'file': 'articles/handy-garment-steamer-best7.html',
        'keyword': '衣類スチーマー ハンディ スチームアイロン 軽量 脱臭',
        'sub_keyword': 'ハンディスチーマー 衣類 アイロン台不要',
        'genre_tag': 'ハンディ衣類スチーマー',
        'key_feature': '立ち上がり数十秒・強力スチーム脱臭除菌',
        'merit': 'アイロン台を出す手間ゼロ。ハンガーにかけたままシワをぐんぐん伸ばし、飲食臭やタバコ臭などのニオイも一掃。',
        'tags': ['立ち上がり数十秒', '大容量連続スチーム', '脱臭・除菌99%', '軽量・手首が疲れない']
    },
    {
        'file': 'articles/handy-vacuum-cleaner-best7.html',
        'keyword': 'ハンディクリーナー コードレス 強力吸引 小型 掃除機 車',
        'sub_keyword': 'ハンディ掃除機 充電式 軽量 コンパクト',
        'genre_tag': '小型ハンディクリーナー',
        'key_feature': '超軽量スリムボディ・超強力サイクロン吸引',
        'merit': 'デスク周りのゴミや車内の小石・砂、ソファのすき間までサッと手に取って即座に清掃。日常の掃除ハードルをゼロにします。',
        'tags': ['超強力吸引力', 'Type-C急速充電', '水洗いHEPAフィルター', '超軽量スリム設計']
    },
    {
        'file': 'articles/ultrasonic-cleaner-glasses-best7.html',
        'keyword': '超音波洗浄機 メガネ 腕時計 小型 洗浄機 卓上',
        'sub_keyword': '超音波クリーナー メガネ洗浄機 小型',
        'genre_tag': '超音波洗浄機',
        'key_feature': '高周波超音波振動・水だけで皮脂汚れ除去',
        'merit': '手洗いでは届かないメガネの鼻あてや時計バンドの隙間に溜まった皮脂・汗・汚れを超微細気泡で根こそぎ浮き上がらせます。',
        'tags': ['高周波超音波振動', 'ワンタッチ自動停止タイマー', 'アクセサリーホルダー付属', '丸洗い可能な安心水槽']
    }
]

def clean_name(raw_name):
    clean = re.sub(r'【[^】]*】', ' ', raw_name)
    clean = re.sub(r'\[[^\]]*\]', ' ', clean)
    clean = re.sub(r'★[^★]*★', ' ', clean)
    clean = re.sub(r'◆[^◆]*◆', ' ', clean)
    clean = re.sub(r'[!！?？／/|｜]', ' ', clean)
    for term in ['送料無料', '即納', 'あす楽', 'ポイント10倍', '公式', '正規品', 'レビュー特典', 'クーポン配布中', 'エントリーでP10倍', '新色追加']:
        clean = clean.replace(term, ' ')
    clean = ' '.join(clean.split())
    return clean[:44]

def fetch_rakuten_items(keyword, needed=7):
    print(f"Fetching Rakuten API for: '{keyword}'...")
    params = {
        'applicationId': app_id,
        'accessKey': access_key,
        'affiliateId': affiliate_id,
        'keyword': keyword,
        'format': 'json',
        'hits': 25,
        'imageFlag': 1
    }
    url = f"{api_url}?{urllib.parse.urlencode(params)}"
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'KurakajiBot/2.0'})
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode('utf-8'))
                raw_items = data.get('Items', [])
                valid_items = []
                seen_codes = set()
                
                for it in raw_items:
                    item = it.get('Item', {})
                    code = item.get('itemCode')
                    name = item.get('itemName', '')
                    price = item.get('itemPrice', 0)
                    aff_url = item.get('affiliateUrl', '')
                    imgs = [img.get('imageUrl') for img in item.get('mediumImageUrls', []) if img.get('imageUrl')]
                    
                    if not code or code in seen_codes:
                        continue
                    if price < 1200 or not imgs or not aff_url:
                        continue
                    if any(ng in name for ng in ['リサイクル', '回収', '部品', 'フィルターのみ', '交換用', 'アタッチメントのみ', '取扱説明書', 'ケースのみ', '洗浄液のみ']):
                        continue
                    
                    hi_img = imgs[0].replace('?_ex=128x128', '?_ex=600x600')
                    
                    seen_codes.add(code)
                    valid_items.append({
                        'code': code,
                        'name': clean_name(name),
                        'raw_name': name,
                        'price': f"{price:,}円",
                        'aff_url': aff_url,
                        'image': hi_img,
                        'shop_name': item.get('shopName', '')
                    })
                    if len(valid_items) == needed:
                        break
                        
                print(f" -> Found {len(valid_items)} verified items.")
                return valid_items
        except urllib.error.HTTPError as e:
            if e.code == 429:
                print(f"Rate limited (429). Retrying in 3s...")
                time.sleep(3)
            else:
                print(f"HTTPError: {e}")
                time.sleep(2)
        except Exception as e:
            print(f"Error: {e}. Retrying in 2s...")
            time.sleep(2)
    return []

for target in targets:
    fpath = target['file']
    print(f"\n==========================================")
    print(f"Processing: {fpath}")
    
    items = fetch_rakuten_items(target['keyword'], needed=7)
    if len(items) < 7:
        print(f"Shortage ({len(items)} items), fetching backup with: '{target['sub_keyword']}'...")
        time.sleep(1.2)
        backup_items = fetch_rakuten_items(target['sub_keyword'], needed=10)
        seen_codes = {it['code'] for it in items}
        for b in backup_items:
            if b['code'] not in seen_codes:
                items.append(b)
                seen_codes.add(b['code'])
            if len(items) == 7:
                break
                
    time.sleep(1.2) # Rate limit courtesy
    
    if len(items) < 7:
        print(f"ERROR: Could not get 7 items for {fpath}! Only got {len(items)}.")
        continue
    
    with open(fpath, 'r', encoding='utf-8') as fp:
        html_content = fp.read()
        
    # Build new rankings-section HTML containing EXACTLY 7 product-item-cards
    rank_colors = [
        '#f59e0b', # 1 Gold
        '#94a3b8', # 2 Silver
        '#d97706', # 3 Bronze
        '#64748b', # 4
        '#64748b', # 5
        '#64748b', # 6
        '#64748b'  # 7
    ]
    
    cards_html = ""
    for idx, it in enumerate(items, 1):
        badge_bg = rank_colors[idx-1]
        
        # Tags formatting
        tags_markup = "".join([f"<span style='background:#f1f5f9;color:#334155;padding:4px 10px;border-radius:6px;font-size:0.8rem;font-weight:600;'>{html.escape(t)}</span>" for t in target['tags']])
        
        card = f"""        <article class="product-item-card" style="display: flex; gap: 24px; background: #fff; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
          <div class="product-gallery" style="flex: 0 0 200px; text-align: center;">
            <div style="background: {badge_bg}; color: #fff; width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 1.1rem; margin-bottom: 12px;">{idx}</div>
            <img src="{it['image']}" alt="{html.escape(it['name'])}" style="width: 100%; max-width: 180px; height: 180px; object-fit: contain; border-radius: 10px; background: #f8fafc;" loading="lazy" />
          </div>
          <div class="product-body" style="flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="rank-header" style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0; line-height: 1.4;">第{idx}位：{html.escape(it['name'])}</h3>
              </div>
              <div style="font-size: 1.35rem; font-weight: 800; color: #e11d48; margin-bottom: 12px;">{it['price']} <span style="font-size: 0.8rem; color: #64748b; font-weight: normal;">(税込・送料無料目安)</span></div>
              <p style="color: #475569; font-size: 0.95rem; line-height: 1.7; margin-bottom: 16px;">{target['merit']}（楽天市場公式取扱店：{html.escape(it['shop_name'])}）</p>
              <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
                {tags_markup}
              </div>
            </div>
            <div>
              <a href="{it['aff_url']}" target="_blank" rel="noopener sponsored" style="display: inline-block; background: linear-gradient(135deg, #e11d48 0%, #be123c 100%); color: #fff; padding: 12px 28px; border-radius: 8px; font-weight: 800; font-size: 0.95rem; text-decoration: none; box-shadow: 0 4px 10px rgba(225,29,72,0.25);">
                🛒 楽天市場で最安値・口コミを見る →
              </a>
            </div>
          </div>
        </article>"""
        cards_html += card + "\n\n"
        
    new_rankings_section = f"""<section class='rankings-section'><h2>【2026年最新】おすすめ人気厳選ラインナップ TOP7</h2>
{cards_html}</section>"""

    # Replace old rankings section
    # Locate <section class='rankings-section'> or <section class="rankings-section">
    pattern = r"<section class=['\"]rankings-section['\"]>.*?</section>"
    if re.search(pattern, html_content, flags=re.DOTALL):
        html_content = re.sub(pattern, new_rankings_section, html_content, count=1, flags=re.DOTALL)
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(html_content)
        print(f"SUCCESS: Updated {fpath} with 7 live Rakuten products!")
    else:
        print(f"ERROR: rankings-section pattern not matched in {fpath}!")

print("\nAll target articles processed.")
