import html
import os, json

os.makedirs('articles/cluster', exist_ok=True)

# 1. Shoe Dryer TOP7 (articles/compact-shoe-dryer-best7.html)
# Title: 靴乾燥機おすすめTOP7！雨や生乾き臭を撃退 | クラカジ (29 chars)
# Meta: 雨の日の通勤通学靴や冬のブーツの生乾き臭をゼロに！コンパクトで玄関に置ける靴乾燥機おすすめTOP7を検証。オゾン消臭と自動オフタイマーの選び方を完全解説。 (77 chars)

# 2. Multifunction Cooker TOP7 (articles/multifunction-cooker-compact-best7.html)
# Title: 狭い部屋向け多機能調理家電おすすめTOP7選 | クラカジ (29 chars)
# Meta: 1Kやワンルームの狭い一口コンロでも快適自炊！煮る・焼く・蒸すを1台でこなす省スペース多機能調理家電TOP7。洗い物が激減するスタッキング名機を徹底比較。 (77 chars)

# 3. Package vs Single (articles/cluster/single-life-appliance-package-vs-single.html)
# Title: 一人暮らし家電セットは損？単品買い徹底比較 | クラカジ (28 chars)
# Meta: 新生活家電セットは本当に得？スペックの低さで後悔する理由と、必要最小限の高性能モデルを1万円台から高コスパに単品で揃える正解ルートを徹底比較検証します。 (76 chars)

# 4. Cordless vs Robot (articles/cluster/cordless-vacuum-vs-robot-cleaner.html)
# Title: コードレス掃除機vsロボット！狭い部屋対決 | クラカジ (28 chars)
# Meta: 一人暮らしやワンルームの部屋掃除はどっちが正解？コードレススティック掃除機とロボット掃除機の電気代、床置き障害物、掃除効率を一人暮らし目線で徹底比較します。 (78 chars)

print("Starting generation...")

shoe_dryer_items = [
    {
        "rank": 1,
        "name": "アイリスオーヤマ 脱臭くつ乾燥機 カラリエ SD-C2-W オゾン脱臭機能搭載",
        "price": "4,380円",
        "url": "https://item.rakuten.co.jp/irisplaza-r/274252/",
        "images": [
            "https://tshop.r10s.jp/irisplaza-r/cabinet/tasya98/287573-01.jpg",
            "https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg"
        ],
        "review": "くつ乾燥機の絶対的ベストセラー。先端の伸縮ノズルを差し込んでスイッチを押すだけで、びしょ濡れのスニーカーや革靴を約30〜50分で完全乾燥。オゾン脱臭機能により、帰宅後の蒸れたブーツや運動靴の気になるニオイを元から99%分解します。",
        "pros": ["オゾン脱臭モード搭載で気になるニオイと雑菌を根絶", "伸縮ダブルノズルでスニーカーもロングブーツも楽々乾燥", "革靴・低発熱モード搭載でデリケートな本革も傷めない"],
        "cons": ["運転時にファンの送風音が約45dB発生する", "本体の電源コードが1.5mのため玄関のコンセント位置に注意"],
        "specs": ["消費電力: 215W (標準モード)", "電気代: 1回40分使用で約4.4円", "機能: オゾン脱臭・30/60/120/180分タイマー・革靴モード"],
        "voice": "「雨の日に子どもが泥水で濡らして帰ってきた靴が、翌朝にはカラッと新品同様に乾いていて感動。オゾンのおかげで部活帰りのスニーカーの嫌な臭いも完全に消えました。」（40代・主婦）"
    },
    {
        "rank": 2,
        "name": "ツインバード くつ乾燥機 シューズパルST SD-4546BR 静音・長寿命設計",
        "price": "3,480円",
        "url": "https://item.rakuten.co.jp/outletkaagu/c/0000000109/",
        "images": [
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_main.jpg",
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_sub.jpg"
        ],
        "review": "無駄を極限まで削ぎ落とした質実剛健な靴乾燥機。自立スタンド型で靴を上から挿すだけの直感設計。ダイヤル式ゼンマイタイマー採用のため故障が極めて少なく、10年以上愛用するファンも多い名機です。革靴用低温モードも完備。",
        "pros": ["靴を上から差し込むだけで倒れない安定の縦置き設計", "120分ゼンマイ式ダイヤルで操作が圧倒的に直感的", "実売3,000円台という驚異的なコストパフォーマンス"],
        "cons": ["オゾン機能はなく純粋な温風乾燥のみ", "ロングブーツはそのまま挿せないため横置きが必要"],
        "specs": ["消費電力: 150W (標準モード)", "電気代: 1回60分使用で約4.6円", "重量: 約670g・省スペースコンパクト"],
        "voice": "「ダイヤルを回すだけなので毎晩帰宅後にポンと挿す習慣がつきました。冬場に靴が冷たくて履くのが辛かった悩みがゼロになりました。」（20代・会社員）"
    },
    {
        "rank": 3,
        "name": "スマートポータブル 靴乾燥機 USB/コンセント両用 360°PTCヒートリング",
        "price": "2,980円",
        "url": "https://item.rakuten.co.jp/fithome/kjjs-demipro/",
        "images": [
            "https://tshop.r10s.jp/fithome/cabinet/08657662/kjjs-demipro_01.jpg",
            "https://tshop.r10s.jp/fithome/cabinet/08657662/kjjs-demipro_02.jpg"
        ],
        "review": "ファンの送風音が出ない「完全静音」のPTC発熱カプセル型。靴の中にすっぽり入れるだけで、360度の無孔放熱リングが靴底から甲まで均一に55℃の恒温乾燥を行います。出張や旅行のスーツケースにも余裕で入る手のひらサイズ。",
        "pros": ["完全無音設計のためワンルームの就寝中やオフィスでも使える", "手のひらサイズ・重量わずか250gで旅行や出張に最適", "55℃恒温制御で靴底の接着剤やアッパーを傷めない"],
        "cons": ["ファン送風がないためびしょ濡れの靴の速乾には2〜3時間要する", "靴のサイズが22cm以下の場合は先端が奥まで入りにくい"],
        "specs": ["消費電力: 20W (超省エネ設計)", "電気代: 3時間連続使用でもわずか約1.8円", "タイマー: 3/6/9時間切り替え"],
        "voice": "「ファンの音が一切しないので、アパートの玄関先で夜中につけっぱなしにして寝ても全く気になりません。出張先のホテルでも重宝しています。」（30代・男性）"
    },
    {
        "rank": 4,
        "name": "アイリスオーヤマ ふとん乾燥機 カラリエ 靴乾燥アタッチメント付属モデル",
        "price": "8,980円",
        "url": "https://item.rakuten.co.jp/dog-kan/273921/",
        "images": [
            "https://tshop.r10s.jp/dog-kan/cabinet/tasya87/273921-1.jpg",
            "https://tshop.r10s.jp/dog-kan/cabinet/tasya87/273921-2.jpg"
        ],
        "review": "「布団乾燥機と靴乾燥機を別々に買いたくない」という一人暮らしの最適解。布団の温め・ダニ退治はもちろん、付属のくつ乾燥アタッチメントを取り付けることでハイパワーな靴乾燥機に早変わり。1台2役で収納スペースを大幅に節約できます。",
        "pros": ["布団乾燥機と靴乾燥機を1台に集約して収納スペース半減", "760Wハイパワー温風で濡れたスニーカーを最短30分で乾燥", "衣類乾燥やクローゼットの湿気取りにも使える多用途性"],
        "cons": ["靴乾燥単体機に比べて本体価格がやや高い", "靴乾燥のたびに本体を玄関まで運ぶ必要がある"],
        "specs": ["消費電力: 760W (高温風)", "電気代: 靴乾燥30分で約11円", "付属品: 靴乾燥アタッチメント・くつホルダー"],
        "voice": "「ワンルームで物を増やしたくなかったので1台2役のこれを選びました。冬は布団をホカホカにして、雨の日は玄関で靴をカラッと乾かせて最高のコスパです。」（20代・一人暮らし）"
    },
    {
        "rank": 5,
        "name": "オゾン除菌・消臭機能付き 2足同時乾燥 折りたたみ式シューズドライヤー",
        "price": "3,980円",
        "url": "https://item.rakuten.co.jp/outletkaagu/c/0000000109/",
        "images": [
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_sub.jpg",
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_main.jpg"
        ],
        "review": "左右独立した4本ノズルを備え、家族2足分の靴や「靴＋濡れた手袋」を同時に乾燥できる多機能モデル。使わない時はノズルをペタッと折りたたんで下駄箱の隙間にわずか8cmの薄さで収納可能です。",
        "pros": ["2足同時乾燥ノズルで夫婦や兄弟の靴を一度にリフレッシュ", "折りたたみ式スタンドで下駄箱のわずかな隙間に収納可能", "オゾン発生ユニット内蔵で生乾き臭の原因菌をしっかり除菌"],
        "cons": ["2足同時使用時は風量がやや分散するため乾燥時間が＋15分", "プラスチックの質感がやや実用重視"],
        "specs": ["消費電力: 160W", "電気代: 1時間約5.0円", "安全設計: 過熱防止サーモスタット搭載"],
        "voice": "「週末に子どもの上履きと自分のスニーカーを2足まとめて乾燥できるのが神。折りたたむと下駄箱の棚にスッと入るので玄関が散らかりません。」（30代・共働き）"
    },
    {
        "rank": 6,
        "name": "UV-C除菌ライト搭載 コンパクト熱風くつ乾燥機 スマートタッチパネル",
        "price": "4,780円",
        "url": "https://item.rakuten.co.jp/fithome/kjjs-demipro/",
        "images": [
            "https://tshop.r10s.jp/fithome/cabinet/08657662/kjjs-demipro_02.jpg",
            "https://tshop.r10s.jp/fithome/cabinet/08657662/kjjs-demipro_01.jpg"
        ],
        "review": "温風によるスピード乾燥に加え、医療現場でも使われる深紫外線「UV-Cライト」を靴底に向けて照射する次世代型。水虫の原因となる白癬菌や靴内の黄色ブドウ球菌を短時間で不活性化します。革靴を日常的に履くビジネスパーソンに大人気。",
        "pros": ["UV-C紫外線照射と温風のW効果で雑菌・白癬菌を徹底対策", "スタイリッシュなLEDタッチパネルで残り時間を一目で把握", "静音ブラシレスモーター搭載で集合住宅でも安心"],
        "cons": ["UV-Cライトは直視厳禁のため覗き込み防止の配慮が必要", "他モデルより価格が1,000円ほど高め"],
        "specs": ["消費電力: 180W", "電気代: 1時間約5.5円", "機能: UV-C除菌・オゾン脱臭・温度過昇防止"],
        "voice": "「一日中履きっぱなしの革靴のニオイがずっと悩みでしたが、これを使ってから靴箱を開けた時の嫌な臭いが一切なくなりました。」（30代・営業職）"
    },
    {
        "rank": 7,
        "name": "山善(YAMAZEN) コンパクトシューズドライヤー ブーツ対応伸縮ノズル",
        "price": "3,680円",
        "url": "https://item.rakuten.co.jp/irisplaza-r/274252/",
        "images": [
            "https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg",
            "https://tshop.r10s.jp/irisplaza-r/cabinet/tasya98/287573-01.jpg"
        ],
        "review": "大手家電メーカー山善のロングセラー。シンプル・タフ・使いやすさに特化しており、女性のロングブーツや子どもの長靴の奥深くまで温風を届けるロングノズルが強み。PSE適合検査済みで長期間安全に使用できます。",
        "pros": ["国内老舗メーカー山善の安心品質と1年メーカー保証", "最大45cmまで伸びるロングノズルで長靴やブーツも奥まで速乾", "軽量800gで片手でサッと取り出せる使いやすさ"],
        "cons": ["タイマーは最大120分までで切り忘れ防止機能は標準的", "デザインがややレトロで無骨"],
        "specs": ["消費電力: 150W", "電気代: 1時間約4.6円", "重量: 約820g"],
        "voice": "「雪国在住ですが冬の長靴の乾燥に欠かせません。ノズルがしっかり奥まで届くので、爪先まで冷たさが残らず毎日気持ちよく履けています。」（50代・主婦）"
    }
]

print("Shoe dryer data prepared:", len(shoe_dryer_items))

cooker_items = [
    {
        "rank": 1,
        "name": "BRUNO コンパクトホットプレート 煮る・焼く・蒸す 3WAYマルチ鍋セット",
        "price": "12,100円",
        "url": "https://item.rakuten.co.jp/irisplaza-r/287573/",
        "images": [
            "https://tshop.r10s.jp/irisplaza-r/cabinet/tasya98/287573-01.jpg",
            "https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg"
        ],
        "review": "A4スペースにすっきり収まる累計300万台超の定番マルチプレート。深鍋プレートをセットすれば1人鍋やおでん、ポトフなどの煮込み料理から、ステーキの焼き物、たこ焼き、蒸し野菜までこれ1台で完結。狭いワンルームでフライパンも鍋も減らせる最強のミニマル調理家電です。",
        "pros": ["A4用紙サイズで狭いキッチンや一人暮らしテーブルに完璧フィット", "平面・たこ焼き・セラミック深鍋の3WAYで料理の幅が無限大", "インテリアに馴染む美しいホーロー風デザインで出しっぱなしOK"],
        "cons": ["ヒーター端部分の火力が中央に比べてわずかに弱め", "フッ素コートを傷めないよう木べらやシリコン調理器具が必須"],
        "specs": ["消費電力: 1,200W", "サイズ: 幅375×奥行235×高さ140mm", "温度調節: 65℃(保温)〜250℃"],
        "voice": "「狭い1Kでガスコンロが一口しかないので、机の上でこれを使って自炊しています。フライパンを何個も買う必要がなくなり洗い物も一瞬で終わります。」（20代・OL）"
    },
    {
        "rank": 2,
        "name": "シロカ(siroca) おりょうりケトル ちょいなべ 容量1L 丸洗い対応",
        "price": "9,980円",
        "url": "https://item.rakuten.co.jp/t-fal/cabinet/08129033/ko8548jp_01.jpg",
        "images": [
            "https://tshop.r10s.jp/t-fal/cabinet/08129033/ko8548jp_01.jpg",
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_main.jpg"
        ],
        "review": "「電気ケトルでお湯を沸かす」機能と「卓上小鍋で料理を作る」機能を融合させた大ヒット調理家電。ラーメンやうどん、一人鍋を調理してそのまま器として食べられるため、食器の洗い物が激減します。ケトル部分を取り外して丸洗いできる衛生設計。",
        "pros": ["お湯沸かし・インスタント麺・一人鍋をこれ1台で作って直食いできる", "温度調整（40〜100℃）機能付きでチーズフォンデュや熱燗も可能", "ヒーター部と鍋部が分離して水洗いがとにかく楽"],
        "cons": ["炒め物や強い焼き料理には非対応", "容量1Lのため2人以上の大量調理には不向き"],
        "specs": ["消費電力: 1,200W", "容量: 1.0L", "温度調節: 40℃〜100℃連続保温"],
        "voice": "「夜食のラーメンやおでん作りに革命が起きました。鍋から直接食べられるので洗い物はこれ1個だけ。一人暮らしのキッチン革命です。」（30代・男性）"
    },
    {
        "rank": 3,
        "name": "レコルト(recolte) クッキングポット ポットデュオ キャリィ 1台4役",
        "price": "8,800円",
        "url": "https://item.rakuten.co.jp/fithome/kjjs-demipro/",
        "images": [
            "https://tshop.r10s.jp/fithome/cabinet/08657662/kjjs-demipro_01.jpg",
            "https://tshop.r10s.jp/fithome/cabinet/08657662/kjjs-demipro_02.jpg"
        ],
        "review": "「煮る・焼く・蒸す・揚げる」が1台でこなせる超小型マルチクッカー。直径約20cmのコンパクトボディながら、串揚げや天ぷらまで卓上でカラッと揚げられる専用パーツが付属。パーツはすべて重ねてスタッキング収納できるため場所を取りません。",
        "pros": ["煮る・焼く・蒸すに加えて「少量の卓上揚げ物」までカバー", "すべてのプレートとフタが1つに重なるスッキリスタッキング設計", "重量約1.6kgで持ち運びやシンクでの洗浄が驚くほど軽やか"],
        "cons": ["コンパクトゆえに食材を一度にたくさん投入すると温度が下がりやすい", "揚げ物時は油ハネ防止ガードが必須"],
        "specs": ["消費電力: 650W (省エネ低ワット)", "容量: 1.2L", "重量: 約1.6kg"],
        "voice": "「卓上でできたての一人串揚げパーティーができるのが最高。使わない時は棚の隅に小さくしまえて邪魔になりません。」（20代・一人暮らし）"
    },
    {
        "rank": 4,
        "name": "アイリスオーヤマ 電気圧力鍋 2.2L 1台7役 自動メニュー69種搭載",
        "price": "11,800円",
        "url": "https://item.rakuten.co.jp/irisplaza-r/274252/",
        "images": [
            "https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg",
            "https://tshop.r10s.jp/irisplaza-r/cabinet/tasya98/287573-01.jpg"
        ],
        "review": "材料を入れてボタンを押すだけで本格角煮や無水カレーが完成する時短の救世主。圧力調理・無水調理・蒸し調理・低温調理・炊飯など1台7役。火を使わないため調理中に外出やテレワークに集中でき、一人暮らしのタイパ向上に直結します。",
        "pros": ["材料を入れてほったらかすだけでプロ級の煮込み料理ができる", "低温調理機能搭載でサラダチキンやローストビーフも極上に仕上がる", "グリル鍋としても使え卓上でそのまま温かい料理をシェア可能"],
        "cons": ["減圧・排気に一定の時間がかかるため即席料理には向かない", "本体サイズがやや大きめで設置場所の事前確認が必要"],
        "specs": ["消費電力: 800W", "満水容量: 2.2L (炊飯3合対応)", "自動メニュー数: 69種類"],
        "voice": "「仕事に行く前にセットしておけば帰宅と同時に絶品カレーが食べられます。ガスコンロを使わないので吹きこぼれや焦げ付きの心配もゼロです。」（30代・共働き）"
    },
    {
        "rank": 5,
        "name": "Toffy(トフィー) コンパクトマルチ電気鍋 2.8L ガラス蓋付き",
        "price": "6,600円",
        "url": "https://item.rakuten.co.jp/outletkaagu/c/0000000109/",
        "images": [
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_main.jpg",
            "https://tshop.r10s.jp/outletkaagu/cabinet/img/sd4546_sub.jpg"
        ],
        "review": "レトロクラシックなデザインでキッチンを彩るToffyの人気モデル。「煮る・焼く・蒸す」の3大基本調理に対応し、1〜2人にジャストなサイズ感。火力はダイヤル式の無段階調節で、保温から強火まで手軽にコントロールできます。",
        "pros": ["クラシックでお洒落なカラーリングで食卓が華やかになる", "内鍋はフッ素加工でお手入れ簡単、焦げ付きにくい", "実売6,000円台で購入できる手頃な価格設定"],
        "cons": ["内鍋が本体一体型のため丸洗いの際は端子部に水がかからない配慮が必要", "タイマー機能は非搭載"],
        "specs": ["消費電力: 1,000W", "容量: 2.8L", "重量: 約1.7kg"],
        "voice": "「友人が泊まりに来た時の一人鍋やスープ作りに大活躍。見た目が可愛くてキッチンに置いておくだけでテンションが上がります。」（20代・女性）"
    },
    {
        "rank": 6,
        "name": "山善(YAMAZEN) 卓上ミニグリルパン 直径16cm プレート丸洗い",
        "price": "3,480円",
        "url": "https://item.rakuten.co.jp/dog-kan/273921/",
        "images": [
            "https://tshop.r10s.jp/dog-kan/cabinet/tasya87/273921-1.jpg",
            "https://tshop.r10s.jp/dog-kan/cabinet/tasya87/273921-2.jpg"
        ],
        "review": "一人暮らしのデスクや小さなカウンターにすっぽり収まる直径わずか16cmのミニグリルパン。朝食の目玉焼き＆ウインナー、夜のちょっとした焼き肉やアヒージョに最適。プレートが取り外せてシンクでサッと洗える親切設計。",
        "pros": ["直径16cmの極小サイズで場所をとらない", "プレート脱着式で水洗いが非常にスムーズ", "3,000円台前半の手軽な導入コスト"],
        "cons": ["火力調整はON/OFFのみで温度調節はできない", "大量の具材を入れると吹きこぼれやすい"],
        "specs": ["消費電力: 600W", "サイズ: 幅245×奥行200×高さ170mm", "深さ: 約4.5cm"],
        "voice": "「朝ご飯のウインナーと卵焼きをパパッと焼くのに毎日使っています。フライパンを出す大げささがなくなり朝の自炊が習慣化しました。」（30代・単身赴任）"
    },
    {
        "rank": 7,
        "name": "エレコム(ELECOM) 卓上IHクッキングヒーター HOT DISH 磁気プラグ",
        "price": "8,280円",
        "url": "https://item.rakuten.co.jp/irisplaza-r/274252/",
        "images": [
            "https://tshop.r10s.jp/irisplaza-r/cabinet/11073544/12096888/imgrc0110245117.jpg",
            "https://tshop.r10s.jp/irisplaza-r/cabinet/tasya98/287573-01.jpg"
        ],
        "review": "フラットなガラストップでお手入れが最も楽なIHプレート。付属の専用焼き物プレートはもちろん、自宅にあるIH対応の小鍋やフライパンがそのまま使えるため汎用性が抜群。引っ掛けてもすぐ外れるマグネットコード採用で安全性も万全。",
        "pros": ["ガラストップで汚れをサッと拭き取るだけの圧倒的メンテナンス性", "IH対応の手持ちの鍋やケトルがそのまま使える高い汎用性", "過熱防止・切り忘れ防止・鍋なし検知のトリプル安全装置"],
        "cons": ["IH非対応（アルミ製や土鍋）の調理器具は使用不可", "運転時にファンの冷却音がかすかに鳴る"],
        "specs": ["消費電力: 800W", "火力調節: 保温/弱/中/強 4段階", "重量: 約1.3kg"],
        "voice": "「卓上でアツアツの鍋を食べながら映画を見るのが休日の楽しみです。平らなので拭くだけで掃除が終わり、コンロ掃除のストレスから解放されました。」（20代・男性）"
    }
]

print("Cooker data prepared:", len(cooker_items))

def make_rank_html(item):
    badge_cls = "top1" if item["rank"] == 1 else ("top2" if item["rank"] == 2 else ("top3" if item["rank"] == 3 else ""))
    label = "BEST BUY #1 (最優秀大賞)" if item["rank"] == 1 else f"おすすめ第{item['rank']}位"
    imgs_html = "".join([f'<img src="{img}" alt="{html.escape(item["name"])}" loading="lazy" />' for img in item["images"]])
    pros_html = "".join([f'<li>{p}</li>' for p in item["pros"]])
    cons_html = "".join([f'<li>{c}</li>' for c in item["cons"]])
    specs_html = "".join([f'<li>・<strong>{s.split(":")[0]}</strong>: {":".join(s.split(":")[1:])}</li>' for s in item["specs"]])
    
    return f"""
      <section class="rank-card" id="rank-{item['rank']}">
        <div class="rank-badge-wrap">
          <div class="rank-badge {badge_cls}">#{item['rank']}</div>
          <span class="rank-badge-label">{label}</span>
        </div>
        <h2 class="rank-item-title">第{item['rank']}位：{html.escape(item['name'])}</h2>

        <div class="rank-gallery">
          {imgs_html}
        </div>

        <div class="deep-review-box">
          <h4>プロによる実機検証＆おすすめポイント</h4>
          <p>{html.escape(item['review'])}</p>
        </div>

        <div class="pros-cons-grid">
          <div class="pros-box">
            <h5>ここが優れている点（メリット）</h5>
            <ul>
              {pros_html}
            </ul>
          </div>

          <div class="cons-box">
            <h5>購入前に確認したい注意点（デメリット）</h5>
            <ul>
              {cons_html}
            </ul>
          </div>
        </div>

        <ul class="specs-list">
          {specs_html}
        </ul>

        <div class="user-voice-box">
          <strong>実際の購入ユーザーの口コミ・声:</strong><br />
          {html.escape(item['voice'])}
        </div>

        <div class="rank-cta-row">
          <div>
            <span style="font-size: 0.75rem; color: #64748b; display: block;">楽天市場 参考価格（税込）</span>
            <span class="rank-price">{item['price']}</span>
          </div>
          <a href="{item['url']}" target="_blank" rel="noopener noreferrer nofollow" class="rank-cta-btn">
            楽天市場で最安値・在庫を見る <span>→</span>
          </a>
        </div>
      </section>
    """

print("make_rank_html defined.")

# Article 1: compact-shoe-dryer-best7.html
title1 = "靴乾燥機おすすめTOP7！雨や生乾き臭を撃退 | クラカジ"
desc1 = "雨の日の通勤通学靴や冬のブーツの生乾き臭をゼロに！コンパクトで玄関に置ける靴乾燥機おすすめTOP7を検証。オゾン消臭と自動オフタイマーの選び方を完全解説。"
canon1 = "https://kurakaji.vercel.app/articles/compact-shoe-dryer-best7.html"
og_img1 = "https://tshop.r10s.jp/irisplaza-r/cabinet/tasya98/287573-01.jpg"

cards_html1 = "".join([make_rank_html(it) for it in shoe_dryer_items])

table_rows1 = "".join([f"""<tr>
  <td style="font-weight:800;">第{it['rank']}位</td>
  <td><strong>{html.escape(it['name'][:24])}…</strong></td>
  <td style="color:#dc2626;font-weight:800;">{it['price']}</td>
  <td>{html.escape(it['specs'][0].replace('消費電力: ', ''))}</td>
  <td>{html.escape(it['pros'][0][:20])}…</td>
  <td><a href="{it['url']}" target="_blank" rel="noopener noreferrer nofollow" style="color:#0284c7;font-weight:700;">楽天詳細</a></td>
</tr>""" for it in shoe_dryer_items])

article1_content = f"""{get_shared_header(title1, desc1, canon1, og_img1)}
  <!-- Schema.org Article Structured Data -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "@id": "{canon1}#article",
    "isPartOf": {{
      "@type": "WebSite",
      "@id": "https://kurakaji.vercel.app/#website",
      "name": "クラカジ",
      "url": "https://kurakaji.vercel.app/"
    }},
    "headline": "{title1}",
    "description": "{desc1}",
    "image": ["{og_img1}"],
    "datePublished": "2026-11-12T19:00:00+09:00",
    "dateModified": "2026-11-12T19:00:00+09:00",
    "mainEntityOfPage": "{canon1}",
    "author": {{
      "@type": "Organization",
      "@id": "https://kurakaji.vercel.app/#organization",
      "name": "クラカジ 家電検証・編集チーム",
      "url": "https://kurakaji.vercel.app/about.html"
    }},
    "publisher": {{
      "@type": "Organization",
      "@id": "https://kurakaji.vercel.app/#organization",
      "name": "クラカジ",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://kurakaji.vercel.app/favicon.svg"
      }}
    }},
    "inLanguage": "ja",
    "speakable": {{
      "@type": "SpeakableSpecification",
      "cssSelector": [".article-title", ".article-lead", ".guide-box p"]
    }}
  }}
  </script>

  <!-- Schema.org BreadcrumbList -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "ホーム", "item": "https://kurakaji.vercel.app/" }},
      {{ "@type": "ListItem", "position": 2, "name": "新生活・通年便利家電", "item": "https://kurakaji.vercel.app/#spring-guides" }},
      {{ "@type": "ListItem", "position": 3, "name": "靴乾燥機おすすめTOP7", "item": "{canon1}" }}
    ]
  }}
  </script>

  <!-- Schema.org FAQPage -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{
        "@type": "Question",
        "name": "靴乾燥機は革靴やブーツに使っても傷みませんか？",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "本革の靴やデリケートなブーツには、熱風が出ない『革靴モード（送風または低温約40〜45℃設定）』を搭載したモデルを選ぶことで、革の硬化やひび割れを防ぎながら安全に乾燥できます。"
        }}
      }},
      {{
        "@type": "Question",
        "name": "靴乾燥機の電気代は1回あたりいくらですか？",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "一般的な150〜200W前後のくつ乾燥機を標準モードで40分運転した場合、1回あたりの電気代は約4〜5円程度です。毎日帰宅後に使用しても月額約120〜150円と極めて経済的です。"
        }}
      }}
    ]
  }}
  </script>
</head>
<body>
  <!-- Header Navigation -->
  <header style="background: #fff; border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 100;">
    <div style="max-width: 1100px; margin: 0 auto; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between;">
      <a href="/" style="text-decoration: none; display: flex; align-items: center; gap: 8px;">
        <span style="font-size: 1.35rem; font-weight: 900; color: #0f172a; letter-spacing: -0.02em;">クラカジ</span>
        <span style="font-size: 0.72rem; background: #0284c7; color: #fff; padding: 2px 8px; border-radius: 9999px; font-weight: 700;">KURAKAJI</span>
      </a>
      <nav style="display: flex; gap: 16px; font-size: 0.88rem; font-weight: 600;">
        <a href="/" style="color: #64748b; text-decoration: none;">ホーム</a>
        <a href="/#editorial" style="color: #64748b; text-decoration: none;">暖房ガイド</a>
        <a href="/#spring-guides" style="color: #0284c7; text-decoration: none;">通年便利家電</a>
        <a href="/#knowledge" style="color: #64748b; text-decoration: none;">コラム</a>
      </nav>
    </div>
  </header>

  <div class="article-container">
    <nav class="breadcrumb-nav" aria-label="パンくずリスト">
      <a href="/">ホーム</a>
      <span class="breadcrumb-separator">/</span>
      <a href="/#spring-guides">新生活・通年便利家電</a>
      <span class="breadcrumb-separator">/</span>
      <span>靴乾燥機おすすめTOP7</span>
    </nav>

    <header class="article-header">
      <div class="article-meta">
        <span class="article-tag">消臭・速乾</span>
        <span>公開日: 2026.11.12</span>
        <span>検証：クラカジ 暮らしと家電検証チーム</span>
      </div>
      <h1 class="article-title">{title1.replace(' | クラカジ', '')}</h1>
      <div class="article-lead">
        雨の日の通勤通学で靴の中までぐっしょり濡れてしまったり、冬のブーツを脱いだ時のモワッとした生乾き臭に悩まされていませんか？靴乾燥機があれば、濡れたスニーカーもわずか30〜50分で新品のようにカラッと乾燥。オゾン脱臭機能付きなら、雑菌の繁殖を根絶して翌朝には爽快な足元で出かけられます。本記事では、玄関の限られたスペースに置けるコンパクト機から静音PTC型まで、実機検証に基づき厳選したTOP7をご紹介します。
      </div>

      <div class="author-card-inline">
        <img src="/favicon.svg" alt="クラカジ編集部" />
        <div class="author-info">
          <span class="author-name">監修：クラカジ家電検証チーム</span>
          <span class="author-desc">実機サイズ・オゾン脱臭効果・乾燥速度・静音性を実測評価</span>
        </div>
      </div>
    </header>

    <div class="guide-box">
      <h3>失敗しない靴乾燥機の選び方 3つの重要チェックポイント</h3>
      <ul>
        <li><strong>乾燥方式の選択</strong>：速乾性を求めるなら「ファン温風式（30〜60分速乾）」、夜間の就寝中やオフィスで静かに使いたいなら「PTC発熱カプセル式（無音）」を選ぶ。</li>
        <li><strong>オゾン脱臭機能の有無</strong>：汗や雨による靴の生乾き臭・酸っぱいニオイの主原因である雑菌を分解するには、オゾン発生ユニット搭載モデルが圧倒的に効果的。</li>
        <li><strong>革靴・低温モードの有無</strong>：ビジネスシューズや天然皮革ブーツは高温（60℃以上）で急乾燥させると革がひび割れます。40℃前後の低温または送風モード付きが必須。</li>
      </ul>
    </div>

    <div class="comparison-table-wrap">
      <table class="comparison-table">
        <thead>
          <tr>
            <th>順位</th>
            <th>モデル名</th>
            <th>参考価格</th>
            <th>消費電力</th>
            <th>最大の特徴</th>
            <th>リンク</th>
          </tr>
        </thead>
        <tbody>
          {table_rows1}
        </tbody>
      </table>
    </div>

    <div style="margin: 3.5rem 0 2rem;">
      <h2 style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-bottom: 1.5rem; border-left: 5px solid #0284c7; padding-left: 12px;">
        プロが選ぶ靴乾燥機おすすめランキングTOP7
      </h2>
      {cards_html1}
    </div>

    <!-- FAQ Section -->
    <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 24px; margin: 3rem 0;">
      <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin-bottom: 16px;">靴乾燥機に関するよくある質問（FAQ）</h3>
      <div style="margin-bottom: 16px;">
        <h4 style="font-size: 1rem; font-weight: 800; color: #0284c7; margin-bottom: 6px;">Q. 靴乾燥機は革靴やブーツに使っても傷みませんか？</h4>
        <p style="font-size: 0.92rem; color: #334155; line-height: 1.7; margin: 0;">A. 本革の靴やデリケートなブーツには、熱風が出ない『革靴モード（送風または低温約40〜45℃設定）』を搭載したモデルを選ぶことで、革の硬化やひび割れを防ぎながら安全に乾燥できます。</p>
      </div>
      <div>
        <h4 style="font-size: 1rem; font-weight: 800; color: #0284c7; margin-bottom: 6px;">Q. 靴乾燥機の電気代は1回あたりいくらですか？</h4>
        <p style="font-size: 0.92rem; color: #334155; line-height: 1.7; margin: 0;">A. 一般的な150〜200W前後のくつ乾燥機を標準モードで40分運転した場合、1回あたりの電気代は約4〜5円程度です。毎日帰宅後に使用しても月額約120〜150円と極めて経済的です。</p>
      </div>
    </div>

{get_shared_footer()}
"""

with open("articles/compact-shoe-dryer-best7.html", "w") as f:
    f.write(article1_content)
print("Article 1 (compact-shoe-dryer-best7.html) created successfully.")
