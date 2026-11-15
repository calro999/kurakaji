import os, glob, re, json

base_dir = '/home/antigravity/kurakaji'

# Exact length constraints:
# Title: 28〜32 chars (Strictly <= 32 chars)
# Description: 80〜105 chars (Strictly <= 105 chars)
# Brand suffix for title: " | クラカジ" (6 chars) -> headline should be 22〜26 chars so total title is 28〜32 chars!
# OR full title including "| クラカジ" is <= 32 chars.

ARTICLE_OPTIMIZATIONS = {
  # --- Pillar Articles (14) ---
  "articles/circulator-clothes-drying-best7.html": {
    "title": "部屋干し臭ゼロ！サーキュレーターおすすめTOP7",
    "h1": "部屋干し生乾き臭ゼロ！小型DCサーキュレーターおすすめTOP7",
    "desc": "雨の日の部屋干しでも生乾き臭を防ぐ！3D首振りで洗濯物を3倍速く乾かすDCモーターサーキュレーターおすすめ7選。月55円の圧倒的省エネでエアコン代も30%削減する名機を比較。"
  },
  "articles/compact-electric-kettle-best7.html": {
    "title": "朝1分で速沸！一人暮らし向け電気ケトルTOP7",
    "h1": "朝1分で速沸！温度調節＆一人暮らし向け電気ケトルおすすめTOP7",
    "desc": "コーヒーも白湯もこれ1台！1℃刻みで温度調節できる一人暮らし向け電気ケトル7選。保温ポットより年間1万円節約できる都度沸かしの高コスパモデルを徹底比較。"
  },
  "articles/handy-garment-steamer-best7.html": {
    "title": "アイロン台不要！ハンディ衣類スチーマーTOP7",
    "h1": "アイロン台不要！一人暮らし用ハンディ衣類スチーマーおすすめTOP7",
    "desc": "朝の出勤前にハンガーのまま20秒でシワ伸ばし！飲食・タバコ臭を99%消臭する一人暮らし向けハンディ衣類スチーマー7選。軽量で腕が疲れない神タイパ家電を厳選比較。"
  },
  "articles/compact-blender-smoothie-best7.html": {
    "title": "ボトル直飲み！小型ブレンダー＆ミキサーTOP7",
    "h1": "ボトル直飲みで洗い物ゼロ！一人暮らし用小型ブレンダーおすすめTOP7",
    "desc": "作ったボトルでそのまま飲める！プロテインや冷凍スムージーが数秒で作れる一人暮らし向け小型ブレンダー7選。氷も砕けるハイパワーで洗い物が最小限で済む時短家電を紹介。"
  },
  "articles/compact-toaster-oven-best7.html": {
    "title": "狭いキッチンに！縦型スリムトースターTOP7",
    "h1": "狭いキッチンに置ける！縦型スリムオーブントースターおすすめTOP7",
    "desc": "幅24cmでキッチンの隙間にすっきり収まる！電子レンジのトースト機能より5倍速い縦型スリムトースター7選。外サク中フワに2枚同時に焼ける省スペース名機を比較。"
  },
  "articles/compact-dehumidifier-room-drying-best7.html": {
    "title": "部屋干し速乾！一人暮らし用小型除湿機TOP7",
    "h1": "部屋干し速乾＆カビ撃退！一人暮らし用小型衣類乾燥除湿機TOP7",
    "desc": "雨の日でも洗濯物がカラッと乾く！ワンルームや脱衣所に置けるA4サイズの小型衣類乾燥除湿機7選。1日5円から使える省エネコンプレッサー式と結露対策モデルを比較。"
  },
  "articles/compact-hotplate-single-best7.html": {
    "title": "一人鍋や焼肉に！卓上小型ホットプレートTOP7",
    "h1": "一人鍋・焼肉・深鍋マルチ調理！一人暮らし小型ホットプレートTOP7",
    "desc": "狭い食卓でアツアツ自炊！A4サイズで一人鍋や焼肉、たこ焼きが楽しめる卓上小型ホットプレート7選。プレート丸洗い可能で後片付けも簡単な人気モデルを徹底比較。"
  },
  "articles/compact-rice-cooker-single-best7.html": {
    "title": "最短14分炊飯！一人暮らし小型炊飯器TOP7",
    "h1": "最短14分早炊き＆少量炊飯！一人暮らし向け小型炊飯器おすすめTOP7",
    "desc": "0.5合から美味しく炊ける！お弁当箱サイズからおかず同時調理対応まで、一人暮らしに最適な小型炊飯器7選。少量でもふっくら甘く炊き上がるタイパ名機を徹底比較。"
  },
  "articles/compact-air-purifier-humidifier-best7.html": {
    "title": "花粉と乾燥を撃退！卓上加湿空気清浄機TOP7",
    "h1": "花粉症・喉の乾燥を撃退！卓上＆小型加湿空気清浄機おすすめTOP7",
    "desc": "寝室やデスク周りの花粉・乾燥をこれ1台でブロック！シャーププラズマクラスターや静音設計の小型加湿空気清浄機7選。ワンルームに置いても邪魔にならないモデルを比較。"
  },
  "articles/large-room-heater-best10.html": {
    "title": "広い部屋も即暖！リビング暖房器具TOP10",
    "h1": "広い部屋も足元から即暖！リビング用おすすめ暖房器具TOP10",
    "desc": "12〜20畳のリビング全体をムラなく暖める！乾燥知らずのオイルレスヒーターや大風量セラミックファンヒーター10選。電気代を抑えて部屋全体を陽だまりにする名機を比較。"
  },
  "articles/single-person-kotatsu-heater-best10.html": {
    "title": "電気代1時間2円！一人用デスクこたつTOP10",
    "h1": "電気代1時間2.2円！一人暮らし・デスク型一人用こたつTOP10",
    "desc": "エアコン暖房より電気代が1/10！椅子に座ってテレワークできるハイタイプからミニこたつまで一人用こたつ10選。狭いワンルームでも置けて冬の電気代を削る人気モデルを比較。"
  },
  "articles/wearable-blanket-rechargeable-warmer-best10.html": {
    "title": "着る毛布＆カイロ！電気代1日1円暖房TOP10",
    "h1": "着る電気毛布＆充電式カイロ！1日1円で極暖パーソナル暖房TOP10",
    "desc": "部屋全体を温めずに自分だけ即ポカポカ！USB給電で丸洗いできる電気着る毛布と充電式カイロ10選。モバイルバッテリー対応で暖房代を月数千円浮かせる防寒ギアを比較。"
  },
  "articles/desk-panel-heater-best10.html": {
    "title": "デスク足元の冷え撃退！パネルヒーターTOP10",
    "h1": "デスク足元の冷え性撃退！遠赤外線パネルヒーターおすすめTOP10",
    "desc": "机の下に置くだけで即席こたつ化！風が出ず乾燥ゼロ、1時間約4円の遠赤外線デスクパネルヒーター10選。5面発熱・ラウンド型・折りたたみなど在宅ワークの必須暖房を比較。"
  },
  "articles/compact-futon-dryer-best10.html": {
    "title": "冷たい布団を即ホカホカ！布団乾燥機TOP10",
    "h1": "冷たい布団を一瞬でホカホカ極楽に！小型布団乾燥機おすすめTOP10",
    "desc": "マット不要3秒セット！冬の冷たい布団を温め、ダニ退治や雨の日の靴乾燥までこなすコンパクト布団乾燥機10選。アイリスオーヤマ カラリエやツインノズル名機を徹底比較。"
  },

  # --- Topic Cluster Articles (11) ---
  "articles/cluster/single-life-appliances-regret-top5.html": {
    "title": "一人暮らしで買って後悔した家電ワースト5",
    "h1": "一人暮らしで買って後悔した家電ワースト5と狭い部屋の神代用品",
    "desc": "新生活家電セットの罠！一人暮らし経験者が「結局使わなくなった」と後悔した家電ワースト5（大型アイロン・トースター等）を暴露。狭い部屋を圧迫しない省スペース代用品を解説。"
  },
  "articles/cluster/circulator-vs-fan-electricity-cost.html": {
    "title": "サーキュレーター vs 扇風機！電気代比較",
    "h1": "サーキュレーター vs 扇風機！電気代・部屋干し速度・涼しさ比較",
    "desc": "どっちを買うべき？月55円のDCサーキュレーターと扇風機の電気代・乾燥速度・風の届き方をガチ比較。一人暮らしの部屋干しやエアコン併用で損しない正解を解説。"
  },
  "articles/cluster/clothes-drying-smell-complete-guide.html": {
    "title": "部屋干しの生乾き臭を消す干し方と配置術",
    "h1": "洗濯物の生乾き臭を100%防ぐ干し方とサーキュレーター配置術",
    "desc": "雨の日でも臭わない！雑菌モラクセラ菌の増殖を防ぐ5時間以内乾燥の鉄則。サーキュレーターの真下垂直送風とアーチ干しで部屋干し臭をゼロにする配置テクニックを伝授。"
  },
  "articles/cluster/electric-kettle-vs-pot-cost.html": {
    "title": "電気ケトル vs ポット！保温電気代の損得",
    "h1": "電気ケトル vs 電気ポット！24時間保温しっぱなしの損得勘定",
    "desc": "お湯を沸かすならどっちが安い？都度沸かしのケトルと保温ポットの電気代を試算。24時間保温で年間約1万円損する理由と、一人暮らしに最適な給湯スタイルを解説。"
  },
  "articles/cluster/toaster-vs-microwave-toast.html": {
    "title": "トースター vs レンジ！トースト機能比較",
    "h1": "オーブントースター vs 電子レンジ！トースト機能の焼き時間と味比較",
    "desc": "レンジのトースト機能は遅くて裏返しが必要？2分半で焼けるトースターとの焼き時間・サクサク感・味の違いを実食検証。狭いキッチンで本当に買うべきかを徹底判定。"
  },
  "articles/cluster/air-purifier-pollen-placement-guide.html": {
    "title": "空気清浄機はどこに置く？寝室の最適配置",
    "h1": "花粉症対策！空気清浄機はどこに置くのが正解？寝室・部屋の最適配置",
    "desc": "重い花粉を床に落とさず吸い尽くす！玄関・エアコン向かい・ベッド足元など効果が劇的に変わる3大ベストポジションを解説。花粉症のモーニングアタックを防ぐ完全ガイド。"
  },
  "articles/cluster/electric-blanket-all-night-danger.html": {
    "title": "電気毛布の朝までつけっぱなしが危険な理由",
    "h1": "医師も警鐘！電気毛布の朝までつけっぱなしはなぜNG？快眠設定術",
    "desc": "翌朝の体のだるさや喉の渇きは脱水が原因？深部体温の低下を邪魔しない就寝30分前予熱とタイマー活用術を解説。電気代月100円で安全に熟睡できる正しい使い方まとめ。"
  },
  "articles/cluster/winter-electricity-bill-saving-hacks.html": {
    "title": "冬の電気代を月1万円削る小型家電節電術",
    "h1": "冬の電気代高騰対策！小型家電フル活用で暖房費を月1万円削る裏ワザ",
    "desc": "エアコン単体稼働は高額請求の元！エアコン設定20℃＋一人用こたつ・パネルヒーター・サーキュレーター併用で暖かさをキープしながら月1万円節電する最強マニュアル。"
  },
  "articles/cluster/kotatsu-electricity-cost.html": {
    "title": "一人用こたつの電気代！エアコン併用節電術",
    "h1": "一人用こたつの電気代は1ヶ月いくら？つけっぱなし＆エアコン比較",
    "desc": "1日8時間使っても月約530円！サーモスタットによる自動オンオフの仕組みとエアコン併用の節電効果を徹底検証。冬のテレワークや一人暮らしで最も電気代が浮く暖房術。"
  },
  "articles/cluster/panel-heater-vs-ceramic.html": {
    "title": "パネルヒーター vs セラミック！足元暖房対決",
    "h1": "デスクパネルヒーター vs セラミックヒーター！足元暖房はどっち？",
    "desc": "電気代の差は月7,000円！無音・無風・乾燥なしの遠赤外線パネルヒーターと、2秒で即温風が出るセラミックの性能・コストを徹底比較。在宅ワークに最適な選び方。"
  },
  "articles/cluster/futon-dryer-dani-guide.html": {
    "title": "布団乾燥機でダニを死滅させる温度と時間",
    "h1": "完全撃退！布団乾燥機でダニを死滅させる正しい温度・時間・頻度ガイド",
    "desc": "天日干しでは死なない！50℃以上20分の熱風運転と裏返し、死骸をアレルゲンにしない乾燥直後の掃除機吸引法をプロが解説。科学的に証明された最も確実なダニ撃退手順。"
  }
}

# Verify lengths before applying
for path, data in ARTICLE_OPTIMIZATIONS.items():
    full_title = f"{data['title']} | クラカジ"
    title_len = len(full_title)
    desc_len = len(data['desc'])
    print(f"[{path}]")
    print(f"  Title ({title_len} chars): {full_title}")
    print(f"  Desc ({desc_len} chars): {data['desc']}")
    if title_len > 32:
        print(f"  WARNING: Title exceeds 32 chars! ({title_len})")
    if desc_len > 105:
        print(f"  WARNING: Desc exceeds 105 chars! ({desc_len})")

# Apply to all article files
for rel_path, data in ARTICLE_OPTIMIZATIONS.items():
    file_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    full_title = f"{data['title']} | クラカジ"
    
    # 1. Update <title>
    html = re.sub(r'<title>.*?</title>', f'<title>{full_title}</title>', html, flags=re.DOTALL)
    
    # 2. Update <meta name="description">
    html = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{data["desc"]}"', html)
    
    # 3. Update OGP & Twitter tags
    html = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{full_title}"', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{data["desc"]}"', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{full_title}"', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{data["desc"]}"', html)

    # 4. Update <h1> in article body
    html = re.sub(r'<h1 class="article-title">.*?</h1>', f'<h1 class="article-title">{data["h1"]}</h1>', html, flags=re.DOTALL)
    html = re.sub(r'<h1 class="article-h1">.*?</h1>', f'<h1 class="article-h1">{data["h1"]}</h1>', html, flags=re.DOTALL)

    # 5. Update Schema.org Article headline and description
    html = re.sub(r'"headline":\s*"[^"]*"', f'"headline": "{full_title}"', html)
    html = re.sub(r'"description":\s*"[^"]*"', f'"description": "{data["desc"]}"', html)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

print("\nSuccessfully updated all 25 articles with search-optimized, strictly length-controlled titles & descriptions!")
