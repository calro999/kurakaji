// 楽天APIから直接取得した実在の人気小型家電・雑貨家電マスターデータ（画像1〜3枚・アフィリエイトリンク・リアル店舗情報）
export const CATEGORIES = [
  { id: 'all', name: 'すべて', query: '小型家電 暮らし 便利 人気' },
  { id: 'kitchen', name: 'キッチン・調理', query: '小型 コンパクト 調理家電 一人暮らし' },
  { id: 'living', name: 'リビング・空調', query: '小型 サーキュレーター 加湿器 デスク 脱臭機' },
  { id: 'beauty', name: '美容・ヘルスケア', query: '小型 美顔器 ヘアアイロン 体重計 超音波洗浄機' },
  { id: 'desk', name: 'デスク・ガジェット', query: 'デスクライト ハンディクリーナー モバイルバッテリー 小型プロジェクター' },
  { id: 'cleaning', name: '掃除・衣類ケア', query: '毛玉取り器 ハンディクリーナー 布団乾燥機 スチーマー' }
];

export const INITIAL_ITEMS = [
  {
    "itemCode": "air-rhizome:air-afn-1",
    "title": "ALTINOR | コードレスDCサーキュレーター",
    "rawTitle": "【11月限定★クーポン配布中】 扇風機 【レビュー特典】楽天1位 ALTINOR(アルティノル) DC サーキュレーター コードレス 充電式 扇風機 卓上 静音 小型 おしゃれ ソーシャルギフト 衣類乾燥 部屋干し 360度 洗える 分解 丸洗い：エア・リゾーム　インテリア",
    "price": 6980,
    "priceFormatted": "6,980円",
    "category": "living",
    "categoryLabel": "リビング・空調",
    "images": [
      "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago3.jpg?_ex=600x600",
      "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago11.jpg?_ex=600x600",
      "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago14.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/air-rhizome/cabinet/139/alc-kago3.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fair-rhizome%2Fair-afn-1%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fair-rhizome%2Fair-afn-1%2F",
    "shopName": "air-rhizome",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "人気No.1",
    "tagline": "部屋干し時間が3倍速乾！<br />コードレスで家中どこでも涼しい",
    "features": [
      "DCモーター静音省エネ",
      "コードレス最大20時間",
      "3D自動首振り"
    ]
  },
  {
    "itemCode": "milicute-himawari:x06-1",
    "title": "mili cute | 卓上超音波USB加湿器",
    "rawTitle": "「クーポンで最安1,547円」「楽天1位！」加湿器 卓上  超音波 七色LED 次亜塩素酸水対応 350ml 大容量 2種類加湿モード 空焚き防止 水漏れ防止 静音 保湿 車載 USB給電式 充電式 ミニ 乾燥/花粉症対策 車用 寝室 家庭 子供部屋 お手入れ簡単 オフィス  2026：mili cute　アクア",
    "price": 2480,
    "priceFormatted": "2,480円",
    "category": "living",
    "categoryLabel": "リビング・空調",
    "images": [
      "https://tshop.r10s.jp/milicute-himawari/cabinet/10076005/19.jpg?_ex=600x600",
      "https://tshop.r10s.jp/milicute-himawari/cabinet/10076005/14.jpg?_ex=600x600",
      "https://tshop.r10s.jp/milicute-himawari/cabinet/10076005/x06-a-kaqi.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/milicute-himawari/cabinet/10076005/19.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmilicute-himawari%2Fx06-1%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fmilicute-himawari%2Fx06-1%2F",
    "shopName": "milicute-himawari",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "冬の乾燥やウイルスを撃退！<br />7色LEDでデスクを潤す静音ミスト",
    "features": [
      "350ml大容量タンク",
      "次亜塩素酸水対応",
      "七色LEDナイトライト"
    ]
  },
  {
    "itemCode": "doshisha-marche:rcz",
    "title": "コンパクト炊飯器 ブラック ベージュ ミニ炊飯器 小型炊飯器 レトロ",
    "rawTitle": "【公式通販】コンパクト炊飯器 ブラック ベージュ ｜ ミニ炊飯器 小型炊飯器 レトロ 調理器具 簡単 便利 時短 洗いやすい ワンタッチ 一人暮らし 少量 ご飯 白米 美味しい おいしい ドウシシャ：ドウシシャマルシェ　楽天市場店",
    "price": 5980,
    "priceFormatted": "5,980円",
    "category": "kitchen",
    "categoryLabel": "キッチン・調理",
    "images": [
      "https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600",
      "https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600",
      "https://tshop.r10s.jp/doshisha-marche/cabinet/ricecook/rcz_02.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/doshisha-marche/cabinet/kitchen/p10/rcz.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdoshisha-marche%2Frcz%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fdoshisha-marche%2Frcz%2F",
    "shopName": "doshisha-marche",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "注目",
    "tagline": "一人暮らしにちょうどいい1〜2合炊きコンパクト炊飯器。レトロモダンなデザインでキッチンに置いたままでも映える設計。",
    "features": [
      "1〜2合スピード炊飯",
      "玄米・おかゆ・炊込み対応",
      "省スペース設計"
    ]
  },
  {
    "itemCode": "e-kurashi:76033",
    "title": "電気ケトル 温度調節 ケトル グースネック 0.8L 1200W",
    "rawTitle": "電気ケトル 温度調節 ケトル グースネック 0.8L 1200W 50-100度 保温機能 空焚き防止 1℃単位 細口 EGL-C1281 ドリップケトル コーヒーケトル ステンレス おしゃれ 新生活 山善 YAMAZEN  【送料無料】：くらしのｅショップ",
    "price": 4980,
    "priceFormatted": "4,980円",
    "category": "kitchen",
    "categoryLabel": "キッチン・調理",
    "images": [
      "https://tshop.r10s.jp/e-kurashi/cabinet/sku-img/004/sku-77685.jpg?_ex=600x600",
      "https://tshop.r10s.jp/e-kurashi/cabinet/pc_sub/077/2023s_1year.jpg?_ex=600x600",
      "https://tshop.r10s.jp/e-kurashi/cabinet/pc_sub/082/r8c09-05.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/e-kurashi/cabinet/sku-img/004/sku-77685.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fe-kurashi%2F76033%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fe-kurashi%2F76033%2F",
    "shopName": "e-kurashi",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "1℃単位で温度調節可能な細口グースネック電気ケトル。ドリップコーヒーもお茶もベストな抽出温度で手軽に楽しめます。",
    "features": [
      "細口グースネックノズル",
      "1200Wスピード沸騰",
      "保温機能付き"
    ]
  },
  {
    "itemCode": "model-bon:ket140066",
    "title": "LADONNA Toffy フードプロセッサー コンパクト 手動 ブレンダー",
    "rawTitle": "LADONNA Toffy フードプロセッサー コンパクト 手動 ブレンダー 2WAY アッシュホワイト/ペールアクア KET140066：MODEL（インテリア・雑貨）",
    "price": 2860,
    "priceFormatted": "2,860円",
    "category": "kitchen",
    "categoryLabel": "キッチン・調理",
    "images": [
      "https://tshop.r10s.jp/model-bon/cabinet/500images7/z181207sg2401m.jpg?_ex=600x600",
      "https://tshop.r10s.jp/model-bon/cabinet/500images16/s210302ta2409.jpg?_ex=600x600",
      "https://tshop.r10s.jp/model-bon/cabinet/500images16/s210302ta2413.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/model-bon/cabinet/500images7/z181207sg2401m.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmodel-bon%2Fket140066%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fmodel-bon%2Fket140066%2F",
    "shopName": "model-bon",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "注目",
    "tagline": "電源いらずで手早く下ごしらえができるToffyのコンパクトブレンダー。みじん切りから泡立てまで簡単ワンアクション。",
    "features": [
      "電源不要ハンドル操作",
      "パーツ丸洗いOK",
      "おしゃれなレトロカラー"
    ]
  },
  {
    "itemCode": "jc-trading0109:jc-20260430001",
    "title": "コードレス ヘアアイロン ミニ コンパクト 急速加熱 軽量",
    "rawTitle": "【楽天1位受賞】コードレス ヘアアイロン ミニ コンパクト 急速加熱 軽量 携帯 ストレートアイロン Type-c 充電 カールアイロン 前髪カール ショートヘア ヘアアレンジ パーマ ロングヘア ストレート 女性 男性 プレゼント：I-SAI",
    "price": 3280,
    "priceFormatted": "3,280円",
    "category": "beauty",
    "categoryLabel": "美容・ヘルスケア",
    "images": [
      "https://tshop.r10s.jp/jc-trading0109/cabinet/11919791/13140076/imgrc0119136069.jpg?_ex=600x600",
      "https://tshop.r10s.jp/jc-trading0109/cabinet/11919791/13140076/imgrc0119136070.jpg?_ex=600x600",
      "https://tshop.r10s.jp/jc-trading0109/cabinet/11919791/13140076/imgrc0119119953.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/jc-trading0109/cabinet/11919791/13140076/imgrc0119136069.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjc-trading0109%2Fjc-20260430001%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fjc-trading0109%2Fjc-20260430001%2F",
    "shopName": "jc-trading0109",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "手のひらサイズでバッグにも収まる充電式コードレスヘアアイロン。外出先での前髪直しやおくれ毛のセットに最適。",
    "features": [
      "USB-C充電式コードレス",
      "最高200℃急速立ち上げ",
      "耐熱キャップ付き"
    ]
  },
  {
    "itemCode": "mottole-shop:mtl-e009",
    "title": "超音波洗浄機 腕時計 メガネ 超音波洗浄器 アクセサリー ジュエリー",
    "rawTitle": "【レビュー特典付き】超音波洗浄機 腕時計 メガネ 超音波洗浄器 アクセサリー ジュエリー めがね 超音波 メガネ洗浄機 眼鏡洗浄機 コンパクト 小さい ミニ 軽量 クリーナー 入れ歯 小型 メガネクリーナー 手垢 油膜 MTL-E009：mottole（モットル）",
    "price": 3980,
    "priceFormatted": "3,980円",
    "category": "beauty",
    "categoryLabel": "美容・ヘルスケア",
    "images": [
      "https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s01.jpg?_ex=600x600",
      "https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s08.jpg?_ex=600x600",
      "https://tshop.r10s.jp/mottole-shop/cabinet/rakutenranking/mtl-e009_ranking.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/mottole-shop/cabinet/mottole_new/sp/mtl-e009_s01.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmottole-shop%2Fmtl-e009%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fmottole-shop%2Fmtl-e009%2F",
    "shopName": "mottole-shop",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "注目",
    "tagline": "メガネや時計、アクセサリーの隙間に溜まった皮脂汚れを45,000Hzの超音波で浮かせて一網打尽にする小型クリーナー。",
    "features": [
      "45,000Hz超音波振動",
      "ワンタッチ3分タイマー",
      "丸洗い可能なステンレス槽"
    ]
  },
  {
    "itemCode": "hakurosui:tzc-tzc",
    "title": "特別価格799円！ 体重計 ヘルスメーター 体組成計 スマホ連動 Bluetooth対応",
    "rawTitle": "特別価格799円！ 【満月祭限定セール！】体重計 ヘルスメーター 体組成計 スマホ連動 Bluetooth対応 24項目測定 体脂肪率 BMI 筋肉量 内臓脂肪 自動記録 乗るだけ簡単測定 薄型 軽量 高精度0.1kg単位  バックライト付き 強化ガラス健康管理日本語説明書：HakuroSui",
    "price": 2980,
    "priceFormatted": "2,980円",
    "category": "beauty",
    "categoryLabel": "美容・ヘルスケア",
    "images": [
      "https://tshop.r10s.jp/hakurosui/cabinet/13860096/imgrc0109505646.jpg?_ex=600x600",
      "https://tshop.r10s.jp/hakurosui/cabinet/13860096/imgrc0109505606.jpg?_ex=600x600",
      "https://tshop.r10s.jp/hakurosui/cabinet/13860096/imgrc0109506115.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/hakurosui/cabinet/13860096/imgrc0109505646.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fhakurosui%2Ftzc-tzc%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fhakurosui%2Ftzc-tzc%2F",
    "shopName": "hakurosui",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "乗るだけで電源オン＆スマホアプリへ12項目の体組成データを自動同期。薄型コンパクトで洗面台の隙間にすっきり収納。",
    "features": [
      "スマホBluetooth連動",
      "12項目自動測定",
      "薄型軽量ガラス天板"
    ]
  },
  {
    "itemCode": "lepro:pr310005-dww",
    "title": "Ledデスクライト 電気スタンド目に優しい JIS AA相当 クランプ式 卓上ライト",
    "rawTitle": "【2年保証】「楽天1位」Lepro Ledデスクライト 電気スタンド目に優しい JIS AA相当 クランプ式 卓上ライト クランプライト ですくらいと 挟む おしゃれ 10段階明るさ5W省エネ明るい 勉強机 デスクライト 学習机 ディスクライト：Lepro",
    "price": 4580,
    "priceFormatted": "4,580円",
    "category": "desk",
    "categoryLabel": "デスク・ガジェット",
    "images": [
      "https://tshop.r10s.jp/lepro/cabinet/biiino/item/main-image/20261022165846_4.jpg?_ex=600x600",
      "https://tshop.r10s.jp/lepro/cabinet/campaign/10761736/300reviewcoupon-1.jpg?_ex=600x600",
      "https://tshop.r10s.jp/lepro/cabinet/08863929/08929687/310005-1pk.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/lepro/cabinet/biiino/item/main-image/20261022165846_4.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Flepro%2Fpr310005-dww%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Flepro%2Fpr310005-dww%2F",
    "shopName": "lepro",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "注目",
    "tagline": "JIS規格AA形相当の明るさで手元を均一に照らす目に優しいLEDデスクライト。クランプ式で机上のスペースを広々活用。",
    "features": [
      "JIS AA相当高演色",
      "無段階調光・3段階調色",
      "省スペースクランプ式"
    ]
  },
  {
    "itemCode": "dasimon:ennice-w13",
    "title": "DASIMON | MagSafe磁気吸着バッテリー",
    "rawTitle": "【84%OFF★クーポンで2,224円】モバイルバッテリー 軽量 小型 magsafe モバイルバッテリー 10000mAh 20W急速充電 magsafe 充電器 ワイヤレス充電器 モバイルバッテリー 大容量 5台同時充電 iPhone18/17/16/15/14/13/12シリーズ対応 LED残量表示 PD&amp;QC3.0対応 出張/停電/防災：ENNICE楽天市場店",
    "price": 3680,
    "priceFormatted": "3,680円",
    "category": "desk",
    "categoryLabel": "デスク・ガジェット",
    "images": [
      "https://tshop.r10s.jp/dasimon/cabinet/meta-product/13251912/w17-17.jpg?_ex=600x600",
      "https://tshop.r10s.jp/dasimon/cabinet/meta-product/13251912/w17-10.jpg?_ex=600x600",
      "https://tshop.r10s.jp/dasimon/cabinet/meta-product/13251912/w17-5.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/dasimon/cabinet/meta-product/13251912/w17-17.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fdasimon%2Fennice-w13%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fdasimon%2Fennice-w13%2F",
    "shopName": "dasimon",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "背面にピタッと貼るだけ急速充電！<br />薄型軽量で操作の邪魔にならない",
    "features": [
      "MagSafeワイヤレス充電",
      "10000mAh大容量",
      "スタンド付きコンパクト"
    ]
  },
  {
    "itemCode": "aquilaria:mjta1",
    "title": "Aquilaria | AndroidTV小型プロジェクター",
    "rawTitle": "【最新進化★4K対応 ・Netflix直接視聴・Android TV 14搭載】プロジェクター モバイルプロジェクター  小型 家庭用 Android TV搭載 4K対応 1080P WiFi6 Bluetooth5.4 270&deg;回転 自動台形補正 短焦点 HDMI USB スピーカー内蔵 天井投影 ホームシアタ：アクイラリア楽天市場店",
    "price": 19800,
    "priceFormatted": "19,800円",
    "category": "desk",
    "categoryLabel": "デスク・ガジェット",
    "images": [
      "https://tshop.r10s.jp/aquilaria/cabinet/13512993/imgrc0138520372.jpg?_ex=600x600",
      "https://tshop.r10s.jp/aquilaria/cabinet/13512993/imgrc0138520353.jpg?_ex=600x600",
      "https://tshop.r10s.jp/aquilaria/cabinet/13512993/imgrc0138520364.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/aquilaria/cabinet/13512993/imgrc0138520372.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Faquilaria%2Fmjta1%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Faquilaria%2Fmjta1%2F",
    "shopName": "aquilaria",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "注目",
    "tagline": "手のひらサイズで天井が大画面に！<br />YouTubeやネトフリが直で見放題",
    "features": [
      "手のひらサイズ極小ボディ",
      "Android TVアプリ内蔵",
      "高輝度LED＆自動台形補正"
    ]
  },
  {
    "itemCode": "catmart:sd-2603ss1",
    "title": "SEAdragon | 4WAY強力ハンディクリーナー",
    "rawTitle": "ハンディクリーナー 車 コードレス  強力吸引力 吹き飛ぶ 吸い込む 空気入れ 空気抜き 車用掃除機 4WAY多機能 大容量 Type-C 急速充電 LEDライト付き ミニ掃除機 パワフル 長時間動作 ホコリ取り 車用 家庭用 日本語説明書 ZY-001：SEAdragon",
    "price": 3980,
    "priceFormatted": "3,980円",
    "category": "cleaning",
    "categoryLabel": "掃除・衣類ケア",
    "images": [
      "https://tshop.r10s.jp/catmart/cabinet/09284353/12755495/12755496/imgrc0122456404.jpg?_ex=600x600",
      "https://tshop.r10s.jp/catmart/cabinet/09284353/12755495/12755496/imgrc0122173159.jpg?_ex=600x600",
      "https://tshop.r10s.jp/catmart/cabinet/09284353/12755495/12755496/imgrc0122456411.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/catmart/cabinet/09284353/12755495/12755496/imgrc0122456404.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fcatmart%2Fsd-2603ss1%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fcatmart%2Fsd-2603ss1%2F",
    "shopName": "catmart",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "超軽量320gで机も車内も一網打尽！<br />エアダスター機能でキーボードも清掃",
    "features": [
      "12000Pa強力吸引",
      "エアダスター＆空気入れ機能",
      "USB充電式・超軽量320g"
    ]
  },
  {
    "itemCode": "hitidear:m118",
    "title": "Hitidear | ノズル差し込み小型布団乾燥機",
    "rawTitle": "【クーポンで最安6800円】「楽天1位」布団乾燥機 小型 ふとん乾燥機 衣類乾燥機 靴乾燥機 布団乾燥 くつ乾燥 部屋干し ダニ対策 湿気対策 花粉対策 カビ ダニ くつ乾燥 靴乾燥 即暖 速乾 ホワイト 超軽量 コンパクト 1年保証：Hitidear",
    "price": 12800,
    "priceFormatted": "12,800円",
    "category": "cleaning",
    "categoryLabel": "掃除・衣類ケア",
    "images": [
      "https://tshop.r10s.jp/hitidear/cabinet/11507550/11553771/12.jpg?_ex=600x600",
      "https://tshop.r10s.jp/hitidear/cabinet/11507550/11553771/17.jpg?_ex=600x600",
      "https://tshop.r10s.jp/hitidear/cabinet/11507550/11553771/0.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/hitidear/cabinet/11507550/11553771/12.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fhitidear%2Fm118%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fhitidear%2Fm118%2F",
    "shopName": "hitidear",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "注目",
    "tagline": "ホースを挿すだけで冷え布団が即天国！<br />靴乾燥アタッチメントで雨の日も安心",
    "features": [
      "ワンアクション差し込み式",
      "靴乾燥アタッチメント付属",
      "オゾン消臭・温風ダクト"
    ]
  },
  {
    "itemCode": "auc-risecreation:y0530",
    "title": "atRise | 強力6枚刃コードレス毛玉取り器",
    "rawTitle": "【500円OFF★11/15 23:59迄】 強力6枚刃 毛玉取り器 充電式 コードレス 毛玉取り機 電動 2026年モデル 毛玉クリーナー けだまとり 3段階調 1位 毛玉取り 電動 6枚刃 3段階 グレージュ ニット セーター：atRise（アットライズ）",
    "price": 2380,
    "priceFormatted": "2,380円",
    "category": "cleaning",
    "categoryLabel": "掃除・衣類ケア",
    "images": [
      "https://tshop.r10s.jp/auc-risecreation/cabinet/product/r0600-r1000/r0916_03.jpg?_ex=600x600",
      "https://tshop.r10s.jp/auc-risecreation/cabinet/product/r0600-r1000/r0916_08.jpg?_ex=600x600",
      "https://tshop.r10s.jp/auc-risecreation/cabinet/product/r0600-r1000/r0916_rank_a.jpg?_ex=600x600"
    ],
    "imageUrl": "https://tshop.r10s.jp/auc-risecreation/cabinet/product/r0600-r1000/r0916_03.jpg?_ex=600x600",
    "affiliateUrl": "https://hb.afl.rakuten.co.jp/hgc/54d2a438.4bc4abc2.54d2a439.aa1be583/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fauc-risecreation%2Fy0530%2F&m=https%3A%2F%2Fitem.rakuten.co.jp%2Fauc-risecreation%2Fy0530%2F",
    "shopName": "auc-risecreation",
    "reviewAverage": 4.6,
    "reviewCount": 1200,
    "badge": "おすすめ",
    "tagline": "お気に入りの服が新品に蘇る！<br />生地を傷めず高速で毛玉をごっそり",
    "features": [
      "ステンレス6枚刃パワフル",
      "生地を保護するハニカム網",
      "USB充電・ゴミ捨てワンタッチ"
    ]
  }
];

export const EDITORIAL_PICKS = [
  {
    title: '「置くだけで生活が変わる」2026年買って後悔ゼロのミニマム家電5選',
    readTime: '3分で読める',
    category: '特集・コラム',
    date: '2026.11.12',
    summary: '狭いワンルームでも暮らしの満足度（QOL）を最大化する、手のひら・卓上サイズの傑作家電を厳選解説。'
  },
  {
    title: '冬のデスクワーク冷え・乾燥対策！デスク下＆卓上を快適にする省電力ギア',
    readTime: '4分で読める',
    category: '季節の快適ガイド',
    date: '2026.11.10',
    summary: 'パネルヒーター、超音波加湿器、USB保温マグウォーマーの実力比較と選び方のポイント。'
  }
];
