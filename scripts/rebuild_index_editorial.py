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
        <span style="font-size: 0.8rem; font-weight: 800; color: #0284c7; letter-spacing: 0.05em; text-transform: uppercase; background: #e0f2fe; padding: 0.25rem 0.8rem; border-radius: var(--radius-full);">🌟 クラカジ編集部 厳選特集＆検証コラム（全25本）</span>
        <h2 style="font-size: 1.65rem; font-weight: 800; color: var(--color-text-main); margin-top: 0.6rem;">暮らしを激変させる厳選小型家電ガイド</h2>
        <p style="color: var(--color-text-muted); font-size: 0.95rem; margin-top: 0.4rem;">一人暮らし・狭い部屋・電気代節約・タイパを極めた名機のみをランキング＆徹底比較。</p>
      </div>

      <!-- Pillar Rankings Grid (12 Pillar Guides) -->
      <h3 style="font-size: 1.3rem; font-weight: 800; color: #0f172a; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 8px;">
        <span>🏆</span> 人気小型家電おすすめランキングTOP7〜10
      </h3>
      <div class="editorial-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-bottom: 3.5rem;">
        
        <!-- 1. Circulator -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #86efac; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0fdf4; font-size: 0.75rem; font-weight: 800; color: #16a34a;">部屋干し速乾＆DC節電</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/circulator-clothes-drying-best7.html" style="color: var(--color-text-main);">【部屋干し臭ゼロ】サーキュレーター衣類乾燥＆DC静音おすすめ人気TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            3D立体首振りで洗濯物が3倍速く乾く！エアコン代を月30%削減するDCモーター静音モデル。
          </p>
          <a href="/articles/circulator-clothes-drying-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #16a34a; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 2. Electric Kettle -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fde047; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fefce8; font-size: 0.75rem; font-weight: 800; color: #ca8a04;">1℃刻み温度調節</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-electric-kettle-best7.html" style="color: var(--color-text-main);">【朝の1分速沸】温度調節＆一人暮らし向け電気ケトルおすすめ人気TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            コーヒーのハンドドリップから白湯・ミルクまで。保温ポットより年間1万円浮く高コスパ機。
          </p>
          <a href="/articles/compact-electric-kettle-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #ca8a04; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 3. Handy Garment Steamer -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #f472b6; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fdf2f8; font-size: 0.75rem; font-weight: 800; color: #db2777;">アイロン台不要・朝20秒</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/handy-garment-steamer-best7.html" style="color: var(--color-text-main);">【シワ伸ばし＆脱臭】一人暮らし用ハンディ衣類スチーマーおすすめTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            ハンガーに掛けたまま数吹きでピシッと復活！飲食・タバコ臭を99%消臭する出勤前タイパ神機。
          </p>
          <a href="/articles/handy-garment-steamer-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #db2777; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 4. Compact Blender -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #34d399; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #ecfdf5; font-size: 0.75rem; font-weight: 800; color: #059669;">洗い物激減・直飲み</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-blender-smoothie-best7.html" style="color: var(--color-text-main);">【ボトル直飲み】一人暮らし用小型ブレンダー・ミキサーおすすめTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            作ったボトルでそのまま飲める！氷も砕けるハイパワーでプロテイン＆スムージー習慣が定着。
          </p>
          <a href="/articles/compact-blender-smoothie-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #059669; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 5. Toaster Oven -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fdba74; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fff7ed; font-size: 0.75rem; font-weight: 800; color: #ea580c;">幅24cm縦型スリム</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-toaster-oven-best7.html" style="color: var(--color-text-main);">【省スペース極小】縦型スリム＆オーブントースターおすすめ人気TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            電子レンジのトースト機能より5倍速い！キッチンの隙間に置けて外サク中フワに焼ける名機。
          </p>
          <a href="/articles/compact-toaster-oven-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #ea580c; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 6. Compact Dehumidifier -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #60a5fa; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #eff6ff; font-size: 0.75rem; font-weight: 800; color: #2563eb;">梅雨・結露・カビ根絶</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-dehumidifier-room-drying-best7.html" style="color: var(--color-text-main);">【部屋干し速乾】一人暮らし用小型衣類乾燥除湿機おすすめ人気TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            ワンルームや脱衣所に置けるA4サイズ！コンプレッサー式で1日5円から湿気を強力除去。
          </p>
          <a href="/articles/compact-dehumidifier-room-drying-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #2563eb; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 7. Compact Hotplate -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fdba74; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fff7ed; font-size: 0.75rem; font-weight: 800; color: #ea580c;">一人鍋・焼肉・たこ焼き</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-hotplate-single-best7.html" style="color: var(--color-text-main);">【卓上アツアツ自炊】一人暮らし向け小型ホットプレート＆深鍋TOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            キッチンに立たずに食卓で調理＆完食！A4サイズのオシャレな深鍋マルチプレート特集。
          </p>
          <a href="/articles/compact-hotplate-single-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #ea580c; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 8. Compact Rice Cooker -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #fed7aa; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fff7ed; font-size: 0.75rem; font-weight: 800; color: #ea580c;">最短14分・少量炊飯</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-rice-cooker-single-best7.html" style="color: var(--color-text-main);">【早炊き＆少量炊飯】一人暮らし小型炊飯器おすすめ人気ランキングTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            お弁当箱サイズからおかず同時調理まで！一人暮らしの自炊が劇的にラクになる名機。
          </p>
          <a href="/articles/compact-rice-cooker-single-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #ea580c; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 9. Air Purifier & Humidifier -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid #bae6fd; box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">花粉撃退＆卓上静音</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-air-purifier-humidifier-best7.html" style="color: var(--color-text-main);">【花粉・乾燥対策】小型加湿空気清浄機おすすめ人気ランキングTOP7</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            シャーププラズマクラスター、Levoit、スチーム加湿まで！春の花粉症対策と喉の乾燥を解決。
          </p>
          <a href="/articles/compact-air-purifier-humidifier-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 10. Large Room Heater -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid var(--color-border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fef2f2; font-size: 0.75rem; font-weight: 800; color: #dc2626;">リビング12〜20畳</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/large-room-heater-best10.html" style="color: var(--color-text-main);">【広い部屋用】リビング暖房器具おすすめ人気ランキングTOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            デロンギオイルヒーターからコロナ石油ファンヒーターまで！乾燥せず陽だまりの温もり。
          </p>
          <a href="/articles/large-room-heater-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #dc2626; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 11. Single Person Kotatsu -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid var(--color-border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fffbeb; font-size: 0.75rem; font-weight: 800; color: #d97706;">電気代1時間2.2円</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/single-person-kotatsu-heater-best10.html" style="color: var(--color-text-main);">【一人暮らし・デスク型】一人用こたつおすすめ人気ランキングTOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            椅子に座れるハイタイプから折りたたみミニこたつまで！テレワークの救世主。
          </p>
          <a href="/articles/single-person-kotatsu-heater-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #d97706; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

        <!-- 12. Compact Futon Dryer -->
        <article style="background: #fff; padding: 1.5rem; border-radius: var(--radius-lg); border: 1.5px solid var(--color-border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fdf4ff; font-size: 0.75rem; font-weight: 800; color: #a855f7;">快眠＆ダニ退治</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.05rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-futon-dryer-best10.html" style="color: var(--color-text-main);">【冷たい布団をホカホカに】コンパクト布団乾燥機おすすめランキングTOP10</a>
          </h3>
          <p style="font-size: 0.85rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 1.25rem; flex: 1;">
            マット不要3秒セット！アイリスオーヤマ カラリエや靴乾燥対応の人気モデル集。
          </p>
          <a href="/articles/compact-futon-dryer-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.65rem 1rem; background: #a855f7; color: #fff; font-weight: 700; font-size: 0.88rem; border-radius: var(--radius-md);">
            ランキングを読む <span>→</span>
          </a>
        </article>

      </div>

      <!-- SEO Topic Cluster Section (13 Cluster Columns) -->
      <div style="margin-top: 2rem; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: var(--radius-xl); padding: 2.5rem 2rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem; flex-wrap: wrap;">
          <span style="background: #2563eb; color: #fff; font-size: 0.75rem; font-weight: 800; padding: 0.3rem 0.75rem; border-radius: 9999px;">実験・検証コラム (全11本)</span>
          <h3 style="font-size: 1.35rem; font-weight: 800; margin: 0; color: #0f172a;">プロが実験・試算した家電のお悩み解決ガイド</h3>
        </div>
        <p style="color: var(--color-text-muted); font-size: 0.92rem; margin-bottom: 1.75rem;">
          電気代のリアルな計算シミュレーションや、買って後悔しないための比較検証コラム。
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
          
          <a href="/articles/cluster/single-life-appliances-regret-top5.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1.5px solid #fecaca; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #dc2626; margin-bottom: 0.4rem;">⚠️ 後悔防止</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">一人暮らしで買って後悔した家電ワースト5と神代用品</div>
            <div style="font-size: 0.82rem; color: #64748b;">新生活セットの罠！アイロンや大型扇風機がいらない理由と代用品。</div>
          </a>

          <a href="/articles/cluster/circulator-vs-fan-electricity-cost.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #0d9488; margin-bottom: 0.4rem;">⚖️ 性能対決</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">サーキュレーター vs 扇風機！電気代・部屋干し速度の違い</div>
            <div style="font-size: 0.82rem; color: #64748b;">月55円の超省エネ！直進ジェット気流と部屋干し乾燥速度を徹底比較。</div>
          </a>

          <a href="/articles/cluster/clothes-drying-smell-complete-guide.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.4rem;">🧼 部屋干し裏ワザ</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">生乾き臭を100%消す干し方＆サーキュレーター配置術</div>
            <div style="font-size: 0.82rem; color: #64748b;">原因菌モラクセラ菌は5時間で増殖！アーチ干しと垂直送風の完全手順。</div>
          </a>

          <a href="/articles/cluster/electric-kettle-vs-pot-cost.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #d97706; margin-bottom: 0.4rem;">💰 電気代試算</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">電気ケトル vs 電気ポット！保温しっぱなしの損得勘定</div>
            <div style="font-size: 0.82rem; color: #64748b;">年間で約1万円以上の電気代差！都度沸かしが圧倒的にお得な理由。</div>
          </a>

          <a href="/articles/cluster/toaster-vs-microwave-toast.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #ea580c; margin-bottom: 0.4rem;">🍞 実食検証</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">トースター vs 電子レンジのトースト機能！焼き時間と味</div>
            <div style="font-size: 0.82rem; color: #64748b;">2分半で焼けるトースターと10分かかる電子レンジ。サクサク感の秘密。</div>
          </a>

          <a href="/articles/cluster/air-purifier-pollen-placement-guide.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.4rem;">🤧 花粉撃退</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">空気清浄機はどこに置く？寝室・ワンルームの最適配置</div>
            <div style="font-size: 0.82rem; color: #64748b;">重い花粉を落とさず吸い尽くす！玄関・エアコン向かいの3大ポジション。</div>
          </a>

          <a href="/articles/cluster/kotatsu-electricity-cost.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.4rem;">📊 電気代検証</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">一人用こたつの電気代は1ヶ月いくら？つけっぱなし＆エアコン比較</div>
            <div style="font-size: 0.82rem; color: #64748b;">1日8時間で月約530円！サーモスタットの仕組みとエアコン併用の節電術。</div>
          </a>

          <a href="/articles/cluster/panel-heater-vs-ceramic.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.4rem;">⚖️ 暖房対決</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">デスクパネルヒーター vs セラミックヒーター！足元暖房はどっち？</div>
            <div style="font-size: 0.82rem; color: #64748b;">電気代差月7,000円！無音・乾燥なしのパネルか、2秒速暖のセラミックか。</div>
          </a>

          <a href="/articles/cluster/futon-dryer-dani-guide.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #a855f7; margin-bottom: 0.4rem;">🛏️ ダニ退治</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">布団乾燥機でダニを死滅させる正しい温度・時間・頻度ガイド</div>
            <div style="font-size: 0.82rem; color: #64748b;">65℃以上の温風でダニ退治モードをかけるコツと、死骸をアレル物質にしない吸引術。</div>
          </a>

          <a href="/articles/cluster/electric-blanket-all-night-danger.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1.5px solid #fecaca; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #dc2626; margin-bottom: 0.4rem;">🛌 睡眠健康</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">電気毛布の朝までつけっぱなしはなぜNG？脱水とだるさ防止術</div>
            <div style="font-size: 0.82rem; color: #64748b;">深部体温の低下を邪魔しない！入眠30分前予熱＋自動切タイマーの黄金律。</div>
          </a>

          <a href="/articles/cluster/winter-electricity-bill-saving-hacks.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.4rem;">💡 月1万円節約</div>
            <div style="font-weight: 800; font-size: 0.95rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">冬の電気代を月1万円削る小型家電フル活用節電マニュアル</div>
            <div style="font-size: 0.82rem; color: #64748b;">エアコン設定20℃＋こたつ・サーキュレーター併用で暖かさと省エネを両立。</div>
          </a>

        </div>
      </div>
    </section>"""

new_html = html[:start_idx] + new_editorial_section + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html successfully updated with 25 articles!")
