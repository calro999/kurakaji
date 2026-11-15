import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the end of editorial-grid to include the new Spring pillars and Topic Clusters
new_cards = """
        <!-- Article 4: Desk Panel Heater -->
        <article style="background: #fff; padding: 1.75rem; border-radius: var(--radius-lg); border: 1.5px solid var(--color-border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column; transition: transform 0.2s, border-color 0.2s;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0fdfa; font-size: 0.75rem; font-weight: 800; color: #0d9488;">電気代1時間5円・無音</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/desk-panel-heater-best10.html" style="color: var(--color-text-main);">【デスク足元冷え性撃退】デスクパネルヒーターおすすめ人気ランキングTOP10</a>
          </h3>
          <p style="font-size: 0.88rem; color: var(--color-text-muted); line-height: 1.65; margin-bottom: 1.5rem; flex: 1;">
            底面発熱・360度ラウンド型で机の下が即座にミニこたつ化！風が出ず乾燥ゼロ、1日40円の超省エネパネルヒーターを厳選。
          </p>
          <a href="/articles/desk-panel-heater-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.7rem 1rem; background: var(--color-brand-primary); color: #fff; font-weight: 700; font-size: 0.9rem; border-radius: var(--radius-md);">
            ランキング記事を読む <span>→</span>
          </a>
        </article>

        <!-- Article 5: Compact Futon Dryer -->
        <article style="background: #fff; padding: 1.75rem; border-radius: var(--radius-lg); border: 1.5px solid var(--color-border); box-shadow: var(--shadow-sm); display: flex; flex-direction: column; transition: transform 0.2s, border-color 0.2s;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fdf4ff; font-size: 0.75rem; font-weight: 800; color: #a855f7;">快眠＆ダニ退治・靴乾燥</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP10厳選</span>
          </div>
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-futon-dryer-best10.html" style="color: var(--color-text-main);">【冬の冷たい布団を一瞬で天国に】コンパクト布団乾燥機おすすめ人気ランキングTOP10</a>
          </h3>
          <p style="font-size: 0.88rem; color: var(--color-text-muted); line-height: 1.65; margin-bottom: 1.5rem; flex: 1;">
            マット不要3秒セット！アイリスオーヤマ カラリエ、ツインノズル、衣類乾燥カバー付きまで、毎晩ホカホカ安眠できる名機集。
          </p>
          <a href="/articles/compact-futon-dryer-best10.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.7rem 1rem; background: var(--color-brand-primary); color: #fff; font-weight: 700; font-size: 0.9rem; border-radius: var(--radius-md);">
            ランキング記事を読む <span>→</span>
          </a>
        </article>

        <!-- Article 6: Compact Rice Cooker (Spring / New Life) -->
        <article style="background: #fff; padding: 1.75rem; border-radius: var(--radius-lg); border: 1.5px solid #fed7aa; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; transition: transform 0.2s, border-color 0.2s;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #fff7ed; font-size: 0.75rem; font-weight: 800; color: #ea580c;">新生活・一人暮らし特集</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-rice-cooker-single-best7.html" style="color: var(--color-text-main);">【早炊き＆少量炊飯】一人暮らし小型炊飯器おすすめ人気ランキングTOP7</a>
          </h3>
          <p style="font-size: 0.88rem; color: var(--color-text-muted); line-height: 1.65; margin-bottom: 1.5rem; flex: 1;">
            最短14分のお弁当箱炊飯器から、同時におかずも作れるレコルトまで！一人暮らしの自炊が劇的にラクになる名機。
          </p>
          <a href="/articles/compact-rice-cooker-single-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.7rem 1rem; background: #ea580c; color: #fff; font-weight: 700; font-size: 0.9rem; border-radius: var(--radius-md);">
            ランキング記事を読む <span>→</span>
          </a>
        </article>

        <!-- Article 7: Air Purifier & Humidifier (Spring / Pollen) -->
        <article style="background: #fff; padding: 1.75rem; border-radius: var(--radius-lg); border: 1.5px solid #bae6fd; box-shadow: var(--shadow-sm); display: flex; flex-direction: column; transition: transform 0.2s, border-color 0.2s;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
            <span style="padding: 0.25rem 0.65rem; border-radius: var(--radius-full); background: #f0f9ff; font-size: 0.75rem; font-weight: 800; color: #0284c7;">花粉撃退＆卓上静音</span>
            <span style="font-size: 0.78rem; color: var(--color-text-muted);">TOP7厳選</span>
          </div>
          <h3 style="font-size: 1.15rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.45;">
            <a href="/articles/compact-air-purifier-humidifier-best7.html" style="color: var(--color-text-main);">【花粉・乾燥対策】小型加湿空気清浄機おすすめ人気ランキングTOP7</a>
          </h3>
          <p style="font-size: 0.88rem; color: var(--color-text-muted); line-height: 1.65; margin-bottom: 1.5rem; flex: 1;">
            シャーププラズマクラスター、Levoit、スチーム加湿まで！春の花粉症対策と喉の乾燥を解決する卓上・小型モデル。
          </p>
          <a href="/articles/compact-air-purifier-humidifier-best7.html" style="display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; width: 100%; padding: 0.7rem 1rem; background: #0284c7; color: #fff; font-weight: 700; font-size: 0.9rem; border-radius: var(--radius-md);">
            ランキング記事を読む <span>→</span>
          </a>
        </article>
      </div>

      <!-- SEO Topic Cluster Section -->
      <div style="margin-top: 4rem; background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: var(--radius-xl); padding: 2.5rem 2rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
          <span style="background: #2563eb; color: #fff; font-size: 0.75rem; font-weight: 800; padding: 0.3rem 0.75rem; border-radius: 9999px;">知って得する検証コラム</span>
          <h3 style="font-size: 1.4rem; font-weight: 800; margin: 0; color: #0f172a;">プロが実験・試算した家電のお悩み解決ガイド</h3>
        </div>
        <p style="color: var(--color-text-muted); font-size: 0.92rem; margin-bottom: 1.75rem;">
          電気代のリアルな計算シミュレーションや、間違えやすい使い方の注意点を徹底深掘り。
        </p>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem;">
          <a href="/articles/cluster/kotatsu-electricity-cost.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm); transition: border-color 0.2s;">
            <div style="font-size: 0.75rem; font-weight: 800; color: #16a34a; margin-bottom: 0.4rem;">📊 電気代検証</div>
            <div style="font-weight: 800; font-size: 0.98rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">一人用こたつの電気代は1ヶ月いくら？つけっぱなし＆エアコン比較</div>
            <div style="font-size: 0.82rem; color: #64748b;">1日8時間で月約530円！サーモスタットの仕組みとエアコン併用の節電術。</div>
          </a>

          <a href="/articles/cluster/panel-heater-vs-ceramic.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm); transition: border-color 0.2s;">
            <div style="font-size: 0.75rem; font-weight: 800; color: #0284c7; margin-bottom: 0.4rem;">⚖️ 性能対決</div>
            <div style="font-weight: 800; font-size: 0.98rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">デスクパネルヒーター vs セラミックヒーター！足元暖房はどっち？</div>
            <div style="font-size: 0.82rem; color: #64748b;">電気代差月7,000円！無音・乾燥なしのパネルか、2秒速暖のセラミックか。</div>
          </a>

          <a href="/articles/cluster/futon-dryer-dani-guide.html" style="background: #fff; padding: 1.25rem 1.5rem; border-radius: var(--radius-md); border: 1px solid #cbd5e1; text-decoration: none; color: inherit; display: block; box-shadow: var(--shadow-sm); transition: border-color 0.2s;">
            <div style="font-size: 0.75rem; font-weight: 800; color: #ea580c; margin-bottom: 0.4rem;">🛡️ 完全撃退マニュアル</div>
            <div style="font-weight: 800; font-size: 0.98rem; color: #0f172a; margin-bottom: 0.4rem; line-height: 1.4;">布団乾燥機でダニを死滅させる正しい温度・時間・頻度ガイド</div>
            <div style="font-size: 0.82rem; color: #64748b;">天日干しでは死なない！50℃以上20分と裏返し運転、掃除機吸引の必須ステップ。</div>
          </a>
        </div>
      </div>
"""

# Replace from Article 4 to the end of editorial-grid
pattern = re.compile(r'<!-- Article 4: Desk Panel Heater -->.*?</div>\s*</section>', re.DOTALL)
if pattern.search(content):
    content = pattern.sub(new_cards + "\n    </section>", content)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated index.html with new articles and cluster section!")
else:
    print("Pattern not found, please check index.html structure.")
