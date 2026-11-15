"""
genres_config.py
クラカジ向け特集ハブページの月別・通年ジャンル定義マスター
"""

# 年間・季節別の自動生成用ハブページ定義（毎月1日に自動判定・新規ハブ生成）
SEASONAL_HUB_TEMPLATES = {
    1: [
        {"slug": "january-winter-extreme-heaters", "title": "【1月厳冬期】極暖ヒーター＆防寒家電おすすめ特集", "category": "防寒・暖房家電", "keywords": ["オイルヒーター", "遠赤外線ヒーター", "電気毛布 洗える", "足温器"]},
        {"slug": "january-compact-air-purifier", "title": "【1月最新】花粉前倒し・ウイルス対策！高機能小型空気清浄機特集", "category": "空気清浄・衛生家電", "keywords": ["小型 空気清浄機", "卓上 脱臭機", "HEPAフィルター 小型"]}
    ],
    2: [
        {"slug": "february-spring-life-rice-cooker", "title": "【2月新生活先取り】一人暮らし向け極小・高速炊飯器おすすめ特集", "category": "キッチン・調理家電", "keywords": ["一人暮らし 炊飯器 0.5合", "1合 炊飯器 小型", "糖質カット 炊飯器 小型"]},
        {"slug": "february-compact-steamer-iron", "title": "【2月最新】新社会人・学生必見！立ち上がり最速ハンディ衣類スチーマー特集", "category": "生活・衣類ケア家電", "keywords": ["ハンディスチーマー 軽量", "衣類スチーマー 脱臭", "コードレス ミニアイロン"]}
    ],
    3: [
        {"slug": "march-new-life-starter-appliances", "title": "【3月春の新生活】一人暮らしワンルームにぴったりなスマート家電特集", "category": "新生活家電セット", "keywords": ["一人暮らし 家電セット 小型", "コンパクト 電子レンジ", "小型 冷蔵庫 静音"]},
        {"slug": "march-cordless-vacuum-stick", "title": "【3月最新】狭い部屋も1台でピカピカ！超軽量コードレス掃除機特集", "category": "掃除・クリーナー家電", "keywords": ["コードレス掃除機 軽量 1kg", "ハンディクリーナー 強力", "スティック掃除機 一人暮らし"]}
    ],
    4: [
        {"slug": "april-desk-gadget-smart-lighting", "title": "【4月新年度】テレワーク・勉強環境を劇的改善するデスク家電特集", "category": "デスク・スマート家電", "keywords": ["LEDデスクライト 目に優しい", "モニタースクリーンバー", "卓上 小型扇風機 静音"]},
        {"slug": "april-compact-coffee-maker", "title": "【4月最新】忙しい朝も至福の一杯！省スペース全自動コーヒーメーカー特集", "category": "キッチン・調理家電", "keywords": ["コンパクト コーヒーメーカー 全自動", "一人暮らし カプセル式 コーヒー", "ミル付き コーヒーメーカー 小型"]}
    ],
    5: [
        {"slug": "may-room-drying-dehumidifier", "title": "【5月梅雨先取り】生乾き臭ゼロ！部屋干し特化型コンパクト除湿機特集", "category": "除湿・乾燥家電", "keywords": ["除湿機 小型 部屋干し", "コンパクト 衣類乾燥除湿機", "コンプレッサー式 除湿機 小型"]},
        {"slug": "may-portable-cooler-neck-fan", "title": "【5月最新】初夏の通勤・お出かけを涼しく！ネッククーラー＆ハンディファン特集", "category": "冷却・ポータブル家電", "keywords": ["ネッククーラー 冷却プレート", "ハンディファン 静音 強風", "腰掛けファン 小型"]}
    ],
    6: [
        {"slug": "june-rainy-season-circulator", "title": "【6月梅雨本番】空気循環と速乾換気！3D首振りサーキュレーター特集", "category": "空調・サーキュレーター", "keywords": ["サーキュレーター 3D首振り 静音", "サーキュレーター 衣類乾燥", "DCモーター サーキュレーター 小型"]},
        {"slug": "june-compact-futon-dryer", "title": "【6月最新】ジメジメ布団をカラッと除菌消臭！コンパクト布団乾燥機特集", "category": "寝具・除湿家電", "keywords": ["布団乾燥機 マットなし 小型", "コンパクト ふとん乾燥機 ダニ退治", "靴乾燥機 アタッチメント 布団"]}
    ],
    7: [
        {"slug": "july-midsummer-spot-cooler", "title": "【7月猛暑対策】工事不要でどこでも冷風！パーソナルスポットクーラー特集", "category": "冷房・冷却家電", "keywords": ["スポットクーラー 小型 工事不要", "卓上 冷風機 強力", "ポータブルクーラー 小型"]},
        {"slug": "july-healthy-compact-blender", "title": "【7月最新】夏のビタミン補給＆ひんやりスムージー！ボトルブレンダー特集", "category": "キッチン・調理家電", "keywords": ["ブレンダー スムージー そのまま飲める", "小型 ジューサー ミキサー", "氷も砕ける 小型ブレンダー"]}
    ],
    8: [
        {"slug": "august-refreshing-ice-maker", "title": "【8月真夏】自宅で最速製氷＆かき氷！夏のひんやりクッキング家電特集", "category": "キッチン・冷却家電", "keywords": ["小型 高速製氷機", "電動ふわふわかき氷器", "アイスクリームメーカー 小型"]},
        {"slug": "august-travel-mobile-gadgets", "title": "【8月最新】旅行・帰省に役立つ！急速充電モバイル電源＆ポータブル家電特集", "category": "ポータブル・トラベル家電", "keywords": ["小型 ポータブル電源 一泊", "GaN 急速充電器 65W", "旅行用 小型スチーマー"]}
    ],
    9: [
        {"slug": "september-autumn-healthy-air-fryer", "title": "【9月食欲の秋】油を使わずサクサク揚げ物！卓上ノンフライヤー特集", "category": "キッチン・ヘルシー調理家電", "keywords": ["ノンフライヤー 小型 一人暮らし", "エアフライヤー 卓上", "電気フライヤー 小型 卓上"]},
        {"slug": "september-autumn-relax-massager", "title": "【9月最新】夏の疲労をじんわり癒す！小型ネック・アイマッサージャー特集", "category": "リラックス・ヘルスケア家電", "keywords": ["アイマッサージャー 温熱 目元", "ネックマッサージャー 小型 コードレス", "筋膜リリースガン 軽量 ミニ"]}
    ],
    10: [
        {"slug": "october-autumn-early-winter-heaters", "title": "【10月秋冷え対策】寒暖差を乗り切る！デスクパネルヒーター＆足元暖房特集", "category": "暖房・パーソナル防寒", "keywords": ["デスクパネルヒーター 遠赤外線", "足元ヒーター 人感センサー 小型", "着る毛布 電気 USB"]},
        {"slug": "october-hotplate-compact-cooking", "title": "【10月最新】おうち鍋・焼き肉を手軽に楽しむ！一人用コンパクトホットプレート特集", "category": "キッチン・卓上調理家電", "keywords": ["コンパクトホットプレート 一人暮らし", "卓上 電気鍋 一人暮らし", "ミニ グリル鍋 深型"]}
    ],
    11: [
        {"slug": "november-winter-heating-super-guide", "title": "【11月最新】暖房器具・ファンヒーターおすすめ特集！即暖＆省エネ人気モデル徹底比較", "category": "暖房・防寒家電", "keywords": ["セラミックファンヒーター 人感センサー", "大風量 セラミックヒーター 小型", "省エネ 暖房器具 小型", "脱衣所 ヒーター ヒートショック対策"]},
        {"slug": "november-humidifier-dryness-prevention", "title": "【11月最新】加湿器おすすめ人気特集！乾燥対策・おしゃれで静音なハイブリッド＆超音波モデル", "category": "加湿・乾燥対策家電", "keywords": ["加湿器 ハイブリッド 大容量 静音", "卓上 加湿器 超音波 おしゃれ", "スチーム式 加湿器 お手入れ簡単", "アロマ加湿器 小型 寝室"]},
        {"slug": "november-compact-kotatsu-warmth", "title": "【11月最新】こたつ・省スペース暖房特集！一人暮らしからリビング向け人気おすすめ", "category": "こたつ・省エネ暖房", "keywords": ["一人暮らし こたつ 省スペース", "パーソナルこたつ デスク型", "こたつ テーブル 長方形 コンパクト", "省エネ こたつヒーター 遠赤外線"]},
        {"slug": "november-electric-blanket-carpet", "title": "【11月最新】電気毛布・ホットカーペット特集！節電＆足元ぬくぬく人気アイテムまとめ", "category": "寝具・電気毛布", "keywords": ["電気毛布 洗える 掛け敷き", "電気ひざ掛け フランネル", "ホットカーペット 1畳 コンパクト", "電気毛布 省エネ タイマー付"]},
        {"slug": "november-clothes-dryer-dehumidifier", "title": "【11月最新】冬の部屋干し・結露対策！速乾衣類乾燥除湿機特集", "category": "除湿・部屋干し家電", "keywords": ["衣類乾燥除湿機 デシカント式 冬", "結露防止 除湿機 小型", "部屋干し スピード乾燥 除湿機"]}
    ],
    12: [
        {"slug": "december-year-end-cleaning-cleaners", "title": "【12月年末大掃除】頑固な汚れもスッキリ！高圧スチームクリーナー＆電動ブラシ特集", "category": "大掃除・清掃家電", "keywords": ["スチームクリーナー 小型 ハンディ", "電動お掃除ブラシ お風呂", "超音波洗浄機 メガネ 小型"]},
        {"slug": "december-winter-party-cooking", "title": "【12月最新】冬のホームパーティーに大活躍！マルチクッカー＆燻製器特集", "category": "キッチン・パーティ調理家電", "keywords": ["電気圧力鍋 コンパクト レシピ付", "マルチグリドル 卓上 小型", "コンパクト 燻製器 家庭用"]}
    ]
}

# 2時間おきにローテーション追加するアクティブ特集のリスト（現在月＋コア人気ジャンル）
ACTIVE_FEATURE_SLUGS = [
    "november-winter-heating-super-guide",
    "november-humidifier-dryness-prevention",
    "november-compact-kotatsu-warmth",
    "november-electric-blanket-carpet",
    "november-clothes-dryer-dehumidifier"
]
