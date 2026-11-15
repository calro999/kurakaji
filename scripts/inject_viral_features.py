import os, glob, re

# 1. Define simulator HTML & JS
SIMULATOR_HTML = """
    <!-- Viral Tool: Winter Electricity Saving Simulator -->
    <section id="simulator" style="margin-top: 4.5rem; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 24px; padding: 3rem 2rem; color: #fff; box-shadow: 0 20px 40px rgba(15,23,42,0.25); border: 1px solid rgba(255,255,255,0.1);">
      <div style="max-width: 780px; margin: 0 auto; text-align: center;">
        <span style="background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid #ef4444; font-size: 0.8rem; font-weight: 800; padding: 0.35rem 1rem; border-radius: 9999px; display: inline-block; margin-bottom: 1rem;">
          ⚡ 10秒でわかる冬の電気代診断
        </span>
        <h2 style="font-size: 1.85rem; font-weight: 900; margin-bottom: 0.75rem; letter-spacing: -0.02em; color: #f8fafc;">
          あなたの冬の暖房代、いくら損してる？<br class="hidden-sm">【節電シミュレーター】
        </h2>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 2.25rem; line-height: 1.6;">
          現在使っているメイン暖房器具と1日の使用時間を選ぶだけ！クラカジ推奨の「一人用こたつ」や「パネルヒーター」に変えた場合の削減額を即座に計算します。
        </p>

        <!-- Form Controls -->
        <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 18px; padding: 2rem; margin-bottom: 2rem; text-align: left;">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem;">
            <div>
              <label style="display: block; font-size: 0.88rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.5rem;">
                ① 現在メインで使っている暖房
              </label>
              <select id="sim-current-heater" style="width: 100%; padding: 0.85rem 1rem; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 0.95rem; font-weight: 600; cursor: pointer;">
                <option value="700">エアコン暖房（平均 700W）</option>
                <option value="1100">セラミックファンヒーター（約 1,100W）</option>
                <option value="1300">オイルヒーター（約 1,300W）</option>
                <option value="400">電気ストーブ・カーボン（約 400W）</option>
                <option value="350">ホットカーペット 2畳（約 350W）</option>
              </select>
            </div>

            <div>
              <label style="display: block; font-size: 0.88rem; font-weight: 700; color: #cbd5e1; margin-bottom: 0.5rem;">
                ② 1日の平均使用時間
              </label>
              <select id="sim-hours" style="width: 100%; padding: 0.85rem 1rem; border-radius: 10px; border: 1px solid #475569; background: #0f172a; color: #fff; font-size: 0.95rem; font-weight: 600; cursor: pointer;">
                <option value="4">4時間（夜間・帰宅後のみ）</option>
                <option value="8" selected>8時間（標準・在宅勤務）</option>
                <option value="12">12時間（休日常時・ロング）</option>
                <option value="16">16時間（ほぼ1日中）</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Result Box -->
        <div id="sim-result-box" style="background: linear-gradient(135deg, rgba(37,99,235,0.15) 0%, rgba(16,185,129,0.15) 100%); border: 2px solid #10b981; border-radius: 18px; padding: 2rem; margin-bottom: 2rem;">
          <div style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0.5rem;">現在の暖房代（1ヶ月・30日計算）</div>
          <div id="sim-current-cost" style="font-size: 1.8rem; font-weight: 900; color: #f87171; margin-bottom: 1.25rem;">約 5,208円 / 月</div>

          <div style="border-top: 1px dashed rgba(255,255,255,0.2); padding-top: 1.25rem;">
            <div style="font-size: 0.95rem; color: #a7f3d0; font-weight: 700; margin-bottom: 0.35rem;">
              🎉 一人用こたつ（弱運転 75W）に切り替えた場合
            </div>
            <div style="display: flex; align-items: baseline; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
              <span style="font-size: 1.1rem; color: #cbd5e1;">月額たったの</span>
              <span id="sim-new-cost" style="font-size: 2rem; font-weight: 900; color: #34d399;">約 558円</span>
              <span style="font-size: 1.25rem; font-weight: 800; color: #fbbf24;">（月 <span id="sim-saved-cost">4,650</span>円 お得！）</span>
            </div>
            <div style="font-size: 0.88rem; color: #94a3b8; margin-top: 0.5rem;">
              ※冬の3ヶ月間で <strong id="sim-winter-saved" style="color: #fbbf24; font-size: 1.1rem;">約 13,950円</strong> の節約になります。
            </div>
          </div>
        </div>

        <!-- Share & Action Buttons -->
        <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
          <a id="sim-share-x" href="#" target="_blank" rel="noopener" style="background: #000; color: #fff; padding: 0.85rem 1.8rem; border-radius: 9999px; font-weight: 800; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none; border: 1px solid #334155; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
            𝕏 診断結果をポストして教える
          </a>
          <a href="/articles/single-person-kotatsu-heater-best10.html" style="background: #2563eb; color: #fff; padding: 0.85rem 1.8rem; border-radius: 9999px; font-weight: 800; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none; box-shadow: 0 4px 15px rgba(37,99,235,0.4);">
            🔥 一人用こたつTOP10を見る →
          </a>
        </div>
      </div>
    </section>
"""

SIMULATOR_SCRIPT = """
<script>
(function() {
  const currentSelect = document.getElementById('sim-current-heater');
  const hoursSelect = document.getElementById('sim-hours');
  const currentCostEl = document.getElementById('sim-current-cost');
  const newCostEl = document.getElementById('sim-new-cost');
  const savedCostEl = document.getElementById('sim-saved-cost');
  const winterSavedEl = document.getElementById('sim-winter-saved');
  const shareBtn = document.getElementById('sim-share-x');

  if (!currentSelect || !hoursSelect) return;

  function recalculate() {
    const watts = parseInt(currentSelect.value, 10);
    const hours = parseInt(hoursSelect.value, 10);
    const kwhPrice = 31; // yen/kWh

    // Current cost (30 days)
    const currentMonthly = Math.round((watts / 1000) * hours * 30 * kwhPrice);

    // Kotatsu cost (75W average)
    const kotatsuMonthly = Math.round((75 / 1000) * hours * 30 * kwhPrice);

    const saved = currentMonthly - kotatsuMonthly;
    const winterSaved = saved * 3;

    currentCostEl.textContent = `約 ${currentMonthly.toLocaleString()}円 / 月`;
    newCostEl.textContent = `約 ${kotatsuMonthly.toLocaleString()}円`;
    savedCostEl.textContent = saved.toLocaleString();
    winterSavedEl.textContent = `約 ${winterSaved.toLocaleString()}円`;

    const selectedHeaterName = currentSelect.options[currentSelect.selectedIndex].text.split('（')[0];
    const tweetText = encodeURIComponent(`冬の暖房代を診断したら、${selectedHeaterName}から「一人用こたつ」に変えるだけで冬3ヶ月で【${winterSaved.toLocaleString()}円】も浮くことが判明…！\\n\\n電気代ヤバい人は10秒で計算できるからやってみて👇\\n`);
    const tweetUrl = encodeURIComponent('https://kurakaji.vercel.app/#simulator');
    shareBtn.href = `https://twitter.com/intent/tweet?text=${tweetText}&url=${tweetUrl}&hashtags=電気代高騰,クラカジ,節電`;
  }

  currentSelect.addEventListener('change', recalculate);
  hoursSelect.addEventListener('change', recalculate);
  recalculate();
})();
</script>
"""

FLOATING_BAR_HTML = """
  <!-- Floating Social Share Bar (Mobile & Desktop) -->
  <aside class="floating-share-bar" aria-label="記事を共有" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; gap: 10px; align-items: center; background: rgba(15,23,42,0.92); backdrop-filter: blur(8px); padding: 8px 14px; border-radius: 9999px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15);">
    <span style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; display: none;" class="share-label">シェア</span>
    <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fkurakaji.vercel.app&text=%E3%80%902026%E6%9C%80%E6%96%B0%E3%80%91%E6%9A%AE%E3%82%89%E3%81%97%E3%82%92%E3%82%B9%E3%83%8E%E3%83%BC%E3%83%88%E3%81%AB%E3%81%99%E3%82%8B%E5%AE%B6%E9%9B%BB%E3%83%A1%E3%83%87%E3%82%A3%E3%82%A2%E3%80%8C%E3%82%AF%E3%83%A9%E3%82%AC%E3%82%B8%E3%80%8D" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #000; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="Xで共有">
      𝕏
    </a>
    <a href="https://social-plugins.line.me/lineit/share?url=https%3A%2F%2Fkurakaji.vercel.app" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #06c755; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="LINEで送る">
      L
    </a>
    <a href="https://b.hatena.ne.jp/entry/s/kurakaji.vercel.app" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #00a4de; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="はてなブックマークに追加">
      B!
    </a>
  </aside>
"""

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

# Add simulator above editorial section
if 'id="simulator"' not in idx:
    idx = idx.replace('<section id="editorial"', SIMULATOR_HTML + '\n    <section id="editorial"')
    # Add simulator script and floating bar before </body>
    idx = idx.replace('</body>', SIMULATOR_SCRIPT + '\n' + FLOATING_BAR_HTML + '\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    print("Injected simulator and floating bar into index.html")

# Update all article html files with floating share bar
article_files = glob.glob('articles/*.html') + glob.glob('articles/cluster/*.html')
for af in article_files:
    with open(af, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'class="floating-share-bar"' not in content:
        # custom share url for each article
        url_match = re.search(r'<link rel="canonical" href="([^"]+)"', content)
        article_url = url_match.group(1) if url_match else "https://kurakaji.vercel.app"
        encoded_url = re.sub(r'[:/]', lambda m: '%3A' if m.group(0)==':' else '%2F', article_url)
        
        custom_bar = f"""
  <!-- Floating Social Share Bar -->
  <aside class="floating-share-bar" aria-label="記事を共有" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; gap: 10px; align-items: center; background: rgba(15,23,42,0.92); backdrop-filter: blur(8px); padding: 8px 14px; border-radius: 9999px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.15);">
    <a href="https://twitter.com/intent/tweet?url={encoded_url}&text=%E3%82%AF%E3%83%A9%E3%82%AC%E3%82%B8%E3%81%AE%E8%A8%98%E4%BA%8B%E3%82%92%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%EF%BC%81" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #000; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="Xで共有">𝕏</a>
    <a href="https://social-plugins.line.me/lineit/share?url={encoded_url}" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #06c755; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="LINEで送る">L</a>
    <a href="https://b.hatena.ne.jp/entry/s/{article_url.replace('https://', '')}" target="_blank" rel="noopener" style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: #00a4de; color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: 900;" title="はてなブックマークに追加">B!</a>
  </aside>
"""
        content = content.replace('</body>', custom_bar + '\n</body>')
        with open(af, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected floating bar into {af}")

print("All viral features successfully injected!")
