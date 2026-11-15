import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<section id="editorial"')
if start_idx == -1:
    print("editorial not found!")
    exit(1)

end_idx = html.find('</section>', start_idx) + len('</section>')

new_editorial_section = """<section id="editorial" style="margin-top: 4.5rem; padding-top: 3rem; border-top: 1px solid var(--color-border);">
      <div style="text-align: center; margin-bottom: 2.25rem;">
        <span style="font-size: 0.8rem; font-weight: 800; color: #0284c7; letter-spacing: 0.05em; text-transform: uppercase; background: #e0f2fe; padding: 0.25rem 0.8rem; border-radius: var(--radius-full);">クラカジ編集部 厳選特集＆検証コラム（全34本）</span>
        <h2 style="font-size: 1.65rem; font-weight: 800; color: var(--color-text-main); margin-top: 0.6rem;">暮らしを激変させる厳選小型家電ガイド</h2>
        <p style="color: var(--color-text-muted); font-size: 0.95rem; margin-top: 0.4rem;">一人暮らし・狭い部屋・電気代節約・タイパを極めた名機のみをランキング＆徹底比較。</p>
      </div>

      <!-- Pillar Rankings Grid (19 Pillar Guides) -->
      <h3 style="font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem;">
        人気小型家電おすすめランキングTOP7〜10
      </h3>
      <div class="editorial-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3.5rem;">
        
        <!-- NEW 1. Shoe Dryer -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #38bdf8; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">オゾン消臭・速乾</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-shoe-dryer-best7.html" style="color: var(--color-text-main);">靴乾燥機おすすめTOP7！雨や生乾き臭を撃退</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            雨で濡れた通勤靴や冬ブーツの生乾き臭をゼロに！玄関に置ける省スペース速乾モデル。
          </p>
          <a href="/articles/compact-shoe-dryer-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- NEW 2. Multifunction Cooker -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #f97316; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fff7ed; font-size: 0.75rem; font-weight: 800; color: #ea580c;">一口コンロ救済</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/multifunction-cooker-compact-best7.html" style="color: var(--color-text-main);">狭い部屋向け多機能調理家電おすすめTOP7選</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            1Kでも快適自炊！煮る・焼く・蒸すを1台でこなして洗い物が激減するスタッキング名機。
          </p>
          <a href="/articles/multifunction-cooker-compact-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #ea580c; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 3. Circulator -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #86efac; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0fdf4; font-size: 0.75rem; font-weight: 800; color: #16a34a;">部屋干し速乾＆DC節電</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/circulator-clothes-drying-best7.html" style="color: var(--color-text-main);">部屋干し臭ゼロ！サーキュレーターおすすめTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            3D立体首振りで洗濯物が3倍速く乾く！エアコン代を月30%削減するDCモーター静音モデル。
          </p>
          <a href="/articles/circulator-clothes-drying-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #16a34a; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 4. Electric Kettle -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fde047; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fefce8; font-size: 0.75rem; font-weight: 800; color: #ca8a04;">1℃刻み温度調節</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-electric-kettle-best7.html" style="color: var(--color-text-main);">朝1分で速沸！一人暮らし向け電気ケトルTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            コーヒーのハンドドリップから白湯・ミルクまで。保温ポットより年間1万円浮く高コスパ機。
          </p>
          <a href="/articles/compact-electric-kettle-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #ca8a04; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 5. Handy Garment Steamer -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #a78bfa; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f5f3ff; font-size: 0.75rem; font-weight: 800; color: #7c3aed;">シワ伸ばし＆脱臭</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/handy-garment-steamer-best7.html" style="color: var(--color-text-main);">アイロン台不要！ハンディ衣類スチーマーTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            立ち上がり20秒！ハンガーにかけたままスーツもブラウスも一瞬でシワなし＆除菌。
          </p>
          <a href="/articles/handy-garment-steamer-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #7c3aed; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 6. Handy Vacuum Cleaner -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #38bdf8; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">500g超軽量＆強吸引</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/handy-vacuum-cleaner-best7.html" style="color: var(--color-text-main);">車や机の掃除に！小型ハンディクリーナーTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            ペットの毛・食べこぼし・車内清掃に。コードレスでサッと吸えるコンパクト掃除機。
          </p>
          <a href="/articles/handy-vacuum-cleaner-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 7. Electric Lint Remover -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #f472b6; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fdf2f8; font-size: 0.75rem; font-weight: 800; color: #db2777;">生地を傷めない</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/electric-lint-remover-best7.html" style="color: var(--color-text-main);">服が新品によみがえる！電動毛玉取り器TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            お気に入りのニットや靴下が復活！USB充電式＆大型刃で短時間でごっそり取れる。
          </p>
          <a href="/articles/electric-lint-remover-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #db2777; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 8. Ultrasonic Cleaner -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #38bdf8; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">皮脂・指紋分解</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/ultrasonic-cleaner-glasses-best7.html" style="color: var(--color-text-main);">メガネや時計の皮脂汚れ落とし！超音波洗浄機TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            水だけで隙間の汚れが浮き出る！メガネ・アクセサリー・入れ歯を新品の輝きに。
          </p>
          <a href="/articles/ultrasonic-cleaner-glasses-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 9. Compact Blender -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #4ade80; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0fdf4; font-size: 0.75rem; font-weight: 800; color: #15803d;">ボトル直飲み・時短</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-blender-smoothie-best7.html" style="color: var(--color-text-main);">ボトル直飲み！小型ブレンダー＆ミキサーTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            作ってそのまま持ち運べる！プロテインや朝のスムージー習慣を挫折しない時短ミキサー。
          </p>
          <a href="/articles/compact-blender-smoothie-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #15803d; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 10. Compact Toaster Oven -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fb923c; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fff7ed; font-size: 0.75rem; font-weight: 800; color: #c2410c;">縦型スリム・外カリ中フワ</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-toaster-oven-best7.html" style="color: var(--color-text-main);">狭いキッチンに！縦型スリムトースターTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            幅20cmの隙間に収まる！高火力ヒーターで冷凍食パンも極上に焼き上げる省スペース機。
          </p>
          <a href="/articles/compact-toaster-oven-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #c2410c; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 11. Compact Dehumidifier -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #38bdf8; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">カビ結露防止＆静音</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-dehumidifier-room-drying-best7.html" style="color: var(--color-text-main);">部屋干し速乾！一人暮らし用小型除湿機TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            ワンルームのジメジメ湿気と生乾き臭を撃退！クローゼットにも置けるペルチェ＆デシカント式。
          </p>
          <a href="/articles/compact-dehumidifier-room-drying-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 12. Compact Hotplate -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #f87171; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fef2f2; font-size: 0.75rem; font-weight: 800; color: #dc2626;">A4サイズ・丸洗いOK</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-hotplate-single-best7.html" style="color: var(--color-text-main);">一人鍋や焼肉に！卓上小型ホットプレートTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            テーブル上でできたて熱々！深鍋・たこ焼き対応で料理の幅が広がる自炊の味方。
          </p>
          <a href="/articles/compact-hotplate-single-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #dc2626; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 13. Compact Rice Cooker -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fbbf24; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fffbeb; font-size: 0.75rem; font-weight: 800; color: #d97706;">0.5〜1.5合・早炊き</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-rice-cooker-single-best7.html" style="color: var(--color-text-main);">最短14分炊飯！一人暮らし小型炊飯器TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            お茶碗1杯分から炊きたて！冷凍ご飯いらずで電気代も安いお弁当箱型＆ミニ炊飯器。
          </p>
          <a href="/articles/compact-rice-cooker-single-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #d97706; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 14. Compact Air Purifier -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #34d399; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #ecfdf5; font-size: 0.75rem; font-weight: 800; color: #059669;">HEPAフィルター除菌</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-air-purifier-humidifier-best7.html" style="color: var(--color-text-main);">花粉と乾燥を撃退！卓上加湿空気清浄機TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            寝室やデスク周りをクリーンに！花粉・ハウスダスト・喉の乾燥を防ぐ1台2役の省スペース機。
          </p>
          <a href="/articles/compact-air-purifier-humidifier-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #059669; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 15. Large Room Heater -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #f87171; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fef2f2; font-size: 0.75rem; font-weight: 800; color: #dc2626;">大風量・節電センサー</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/large-room-heater-best10.html" style="color: var(--color-text-main);">広い部屋も即暖！リビング暖房器具TOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            8〜15畳のリビングをムラなく速暖！人感・室温Wセンサーで電気代を抑える最新ヒーター。
          </p>
          <a href="/articles/large-room-heater-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #dc2626; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 16. Single Person Kotatsu -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fbbf24; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fffbeb; font-size: 0.75rem; font-weight: 800; color: #d97706;">1時間2円・テレワーク</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/single-person-kotatsu-heater-best10.html" style="color: var(--color-text-main);">電気代1時間2円！一人用デスクこたつTOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            椅子に座って快適作業！掛け布団付き3点セットで下半身を包み込む究極の省エネ暖房。
          </p>
          <a href="/articles/single-person-kotatsu-heater-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #d97706; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 17. Compact Futon Dryer -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #a855f7; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #faf5ff; font-size: 0.75rem; font-weight: 800; color: #9333ea;">ダニ退治・即ホカホカ</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-futon-dryer-best10.html" style="color: var(--color-text-main);">冷たい布団を即ホカホカ！布団乾燥機TOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            マット不要ノズル差し込み式！冬の冷え切った布団を20分で天国に変える快眠必須ギア。
          </p>
          <a href="/articles/compact-futon-dryer-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #9333ea; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 18. Desk Panel Heater -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #38bdf8; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">無音・足元ポカポカ</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/desk-panel-heater-best10.html" style="color: var(--color-text-main);">デスク足元の冷え撃退！パネルヒーターTOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            折りたたみ式で隙間に収納！遠赤外線で膝下を四方から包み込み、1時間約4円で省エネ暖房。
          </p>
          <a href="/articles/desk-panel-heater-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 19. Wearable Blanket -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #f472b6; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fdf2f8; font-size: 0.75rem; font-weight: 800; color: #db2777;">1日1円・全身発熱</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/wearable-blanket-rechargeable-warmer-best10.html" style="color: var(--color-text-main);">着る毛布＆カイロ！電気代1日1円暖房TOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            USB給電ヒーター内蔵！部屋中どこでも着たまま移動できてエアコン代を劇的に削る暖房ギア。
          </p>
          <a href="/articles/wearable-blanket-rechargeable-warmer-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #db2777; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

      </div>

      <!-- Cluster Columns Grid (15 Cluster Columns) -->
      <h3 style="font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem;">
        家電の選び方・電気代比較・失敗回避コラム（全15本）
      </h3>
      <div class="editorial-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        
        <!-- NEW 1. Package vs Single -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.5rem;">新生活・損得比較</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/single-life-appliance-package-vs-single.html" style="color: var(--color-text-main);">一人暮らし家電セットは損？単品買い徹底比較</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            セット品の罠を暴露！冷凍室の狭さや旧式レンジを避け、1万円台から高コスパに揃える正解ルート。
          </p>
          <a href="/articles/cluster/single-life-appliance-package-vs-single.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- NEW 2. Cordless vs Robot -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.5rem;">掃除効率対決</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/cordless-vacuum-vs-robot-cleaner.html" style="color: var(--color-text-main);">コードレス掃除機vsロボット！狭い部屋対決</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            ワンルームや1Kでルンバは不要？清掃速度・段差対応・電気代を一人暮らし目線で徹底比較。
          </p>
          <a href="/articles/cluster/cordless-vacuum-vs-robot-cleaner.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 3. Regret Top 5 -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #dc2626; margin-bottom: 0.5rem;">後悔回避</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/single-life-appliances-regret-top5.html" style="color: var(--color-text-main);">一人暮らしで買って後悔した家電ワースト5</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            新生活セットの罠！大型アイロンや安価な掃除機など使わなくなる粗大ゴミを事前回避。
          </p>
          <a href="/articles/cluster/single-life-appliances-regret-top5.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 4. Circulator vs Fan -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.5rem;">電気代検証</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/circulator-vs-fan-electricity-cost.html" style="color: var(--color-text-main);">サーキュレーター vs 扇風機！電気代比較</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            風の直進性と拡散性の違いを徹底検証。エアコン併用で最も節電できる配置術を公開。
          </p>
          <a href="/articles/cluster/circulator-vs-fan-electricity-cost.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 5. Dehumidifier vs AC Dry -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.5rem;">部屋干し比較</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/dehumidifier-vs-ac-dry-cost.html" style="color: var(--color-text-main);">除湿機 vs エアコン除湿！電気代と乾燥速度比較</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            部屋干しの電気代はどっちが安い？コンプレッサー式除湿機とエアコン再熱除湿を徹底計測。
          </p>
          <a href="/articles/cluster/dehumidifier-vs-ac-dry-cost.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 6. Compact Rice Cooker Tasty Guide -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #ca8a04; margin-bottom: 0.5rem;">自炊裏ワザ</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/compact-rice-cooker-tasty-guide.html" style="color: var(--color-text-main);">小型炊飯器でご飯を極上に炊く裏ワザ完全ガイド</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            安価なマイコン式でも料亭の味に！浸水時間・氷1個・みりん小さじ1杯でふっくら炊き上げるコツ。
          </p>
          <a href="/articles/cluster/compact-rice-cooker-tasty-guide.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 7. Clothes Drying Smell Guide -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.5rem;">生乾き撃退</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/clothes-drying-smell-complete-guide.html" style="color: var(--color-text-main);">部屋干しの生乾き臭を消す干し方と配置術</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            5時間以内の乾燥が鉄則！アーチ干しとサーキュレーター送風でモラクセラ菌の増殖をブロック。
          </p>
          <a href="/articles/cluster/clothes-drying-smell-complete-guide.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 8. Electric Kettle vs Pot Cost -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #ca8a04; margin-bottom: 0.5rem;">光熱費比較</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/electric-kettle-vs-pot-cost.html" style="color: var(--color-text-main);">電気ケトル vs ポット！保温電気代の損得</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            魔法瓶保温ポットの電気代は月900円！都度沸かしのケトルとどちらが得か徹底検証。
          </p>
          <a href="/articles/cluster/electric-kettle-vs-pot-cost.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 9. Toaster vs Microwave Toast -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #ea580c; margin-bottom: 0.5rem;">パン焼き比較</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/toaster-vs-microwave-toast.html" style="color: var(--color-text-main);">トースター vs レンジ！トースト機能比較</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            電子レンジのトースト機能は時間がかかり裏返しが必要？専用小型トースターの価値を検証。
          </p>
          <a href="/articles/cluster/toaster-vs-microwave-toast.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 10. Air Purifier Placement Guide -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.5rem;">花粉撃退配置</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/air-purifier-pollen-placement-guide.html" style="color: var(--color-text-main);">空気清浄機はどこに置く？寝室の最適配置</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            部屋の隅は逆効果！玄関からの花粉侵入を防ぐドア正面配置とエアコン気流の連携術。
          </p>
          <a href="/articles/cluster/air-purifier-pollen-placement-guide.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 11. Kotatsu Electricity Cost -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #d97706; margin-bottom: 0.5rem;">暖房節電</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/kotatsu-electricity-cost.html" style="color: var(--color-text-main);">一人用こたつの電気代！エアコン併用節電術</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            エアコンの設定温度を3℃下げて月4,500円浮く！一人用こたつ併用の驚異的な節電効果。
          </p>
          <a href="/articles/cluster/kotatsu-electricity-cost.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 12. Panel Heater vs Ceramic -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.5rem;">足元暖房</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/panel-heater-vs-ceramic.html" style="color: var(--color-text-main);">パネルヒーター vs セラミック！足元暖房対決</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            温風の乾燥と無音遠赤外線の違いを比較。テレワークや狭いデスク下での快適性を検証。
          </p>
          <a href="/articles/cluster/panel-heater-vs-ceramic.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 13. Futon Dryer Dani Guide -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #9333ea; margin-bottom: 0.5rem;">ダニ完全退治</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/futon-dryer-dani-guide.html" style="color: var(--color-text-main);">布団乾燥機でダニを死滅させる温度と時間</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            天日干しではダニは死なない！65℃以上の高温風を隅々まで行き渡らせる掛け布団密閉術。
          </p>
          <a href="/articles/cluster/futon-dryer-dani-guide.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 14. Electric Blanket All Night Danger -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #dc2626; margin-bottom: 0.5rem;">快眠・健康</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/electric-blanket-all-night-danger.html" style="color: var(--color-text-main);">電気毛布の朝までつけっぱなしが危険な理由</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            脱水症状と睡眠の質低下を防ぐタイマー活用法。就寝前30分の予熱で朝まで熟睡できるコツ。
          </p>
          <a href="/articles/cluster/electric-blanket-all-night-danger.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

        <!-- 15. Winter Electricity Bill Saving Hacks -->
        <article style="background: #fff; padding: 1.25rem; border-radius: var(--radius-lg); border: 1.5px solid #cbd5e1; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <span style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.5rem;">節電完全攻略</span>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-bottom: 0.5rem; line-height: 1.4;">
            <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="color: var(--color-text-main);">冬の電気代を月1万円削る小型家電節電術</a>
          </h4>
          <p style="font-size: 0.82rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1rem; flex: 1;">
            高騰する冬の電気代を小型家電の組み合わせで劇的にカットするプロの実践テクニック。
          </p>
          <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="color: #0284c7; font-weight: 700; font-size: 0.85rem; text-decoration: none;">解説記事を読む →</a>
        </article>

      </div>
    </section>"""

new_html = html[:start_idx] + new_editorial_section + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html rebuilt with 34 articles editorial section!")
