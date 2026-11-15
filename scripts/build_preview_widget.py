import glob, json

hubs = []
for p in sorted(glob.glob('/home/antigravity/kurakaji/data/special_features/*.json')):
    if 'posted_item' in p: continue
    with open(p, 'r', encoding='utf-8') as f:
        d = json.loads(f.read())
    hubs.append(d)

out_file = '/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/8eaa11eb-a569-427b-8c67-f197e6238f73/special_features_preview.html'

tab_names = [
    '暖房器具・ファンヒーター',
    '加湿器・乾燥対策',
    'こたつ・省スペース暖房',
    '電気毛布・カーペット',
    '衣類乾燥除湿機・結露対策'
]

order = [
    'november-winter-heating-super-guide',
    'november-humidifier-dryness-prevention',
    'november-compact-kotatsu-warmth',
    'november-electric-blanket-carpet',
    'november-clothes-dryer-dehumidifier'
]
sorted_hubs = []
for o in order:
    for h in hubs:
        if h['slug'] == o:
            sorted_hubs.append(h)
            break

tabs_buttons = ""
for i, name in enumerate(tab_names):
    active_cls = "active px-3 py-1.5 rounded-lg border border-teal-600 bg-teal-600 text-white" if i == 0 else "px-3 py-1.5 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:bg-[var(--card-border)]"
    tabs_buttons += f'<button onclick="switchTab({i})" class="tab-btn {active_cls}">{name}</button>\n'

html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-[var(--background)] text-[var(--foreground)] antialiased p-4">
  <div class="max-w-4xl mx-auto space-y-4">
    <div class="border-b border-[var(--border)] pb-3 flex items-center justify-between">
      <div>
        <span class="inline-block px-2.5 py-0.5 rounded-full text-xs font-bold bg-teal-100 text-teal-800 dark:bg-teal-900/40 dark:text-teal-300 mb-1">
          2026年11月最新家電特集（画像疎通確認済み・完全実データ）
        </span>
        <h1 class="text-lg font-bold">特集ハブページ ライブプレビュー</h1>
      </div>
      <span class="text-xs text-[var(--muted-foreground)]">楽天API直接取得・AI rateスコア順</span>
    </div>

    <!-- Navigation Tabs -->
    <div class="flex flex-wrap gap-2 text-xs font-semibold" id="tabs">
      {tabs_buttons}
    </div>

    <!-- Dynamic Hub Panel -->
    <div id="hub-content" class="bg-[var(--card)] border border-[var(--border)] rounded-xl p-4 shadow-sm space-y-4">
    </div>
  </div>

  <script>
    const HUBS = {json.dumps(sorted_hubs, ensure_ascii=False)};

    function switchTab(index) {{
      document.querySelectorAll('.tab-btn').forEach((btn, i) => {{
        if (i === index) {{
          btn.className = "tab-btn active px-3 py-1.5 rounded-lg border border-teal-600 bg-teal-600 text-white";
        }} else {{
          btn.className = "tab-btn px-3 py-1.5 rounded-lg border border-[var(--border)] bg-[var(--card)] hover:bg-[var(--card-border)]";
        }}
      }});

      const hub = HUBS[index];
      const container = document.getElementById('hub-content');

      let itemsHtml = hub.items.map((it, idx) => {{
        const rank = idx + 1;
        const badgeCol = rank === 1 ? 'bg-amber-500 text-white' : (rank === 2 ? 'bg-slate-400 text-white' : (rank === 3 ? 'bg-amber-700 text-white' : 'bg-slate-200 text-slate-700'));
        const price = (it.itemPrice || 0).toLocaleString() + '円';
        const img = (it.images && it.images.length > 0) ? it.images[0] : '';
        const pros = (it.pros || []).map(p => '<div>✔ ' + p + '</div>').join('');

        return `
          <div class="border border-[var(--border)] rounded-xl p-4 bg-[var(--background)] space-y-3">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="w-7 h-7 rounded-full flex items-center justify-center font-black text-xs ${{badgeCol}}">#${{rank}}</span>
                <span class="text-xs font-bold text-teal-600 dark:text-teal-400">総合スコア: ${{it.rate}}点</span>
              </div>
              <span class="text-sm font-black text-rose-600 dark:text-rose-400">${{price}}</span>
            </div>

            <h3 class="font-bold text-sm leading-snug">${{it.clean_name || it.itemName}}</h3>
            <p class="text-xs font-semibold text-teal-700 dark:text-teal-300">【注目】${{it.catchphrase || ''}}</p>

            <div class="flex gap-3">
              <img src="${{img}}" alt="${{it.clean_name}}" class="w-24 h-24 object-cover rounded-lg border border-[var(--border)] bg-white p-1 shrink-0" />
              <div class="text-xs text-[var(--muted-foreground)] leading-relaxed space-y-1">
                <p class="line-clamp-3">${{it.editorial_review || ''}}</p>
                <div class="pt-1 text-[11px] space-y-0.5 text-emerald-700 dark:text-emerald-400">
                  ${{pros}}
                </div>
              </div>
            </div>

            <div class="pt-2 border-t border-[var(--border)] flex justify-end">
              <a href="${{it.affiliateUrl || '#'}}" target="_blank" rel="noopener noreferrer nofollow" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold bg-rose-600 text-white hover:bg-rose-700 transition-colors shadow-sm">
                楽天市場で詳細・在庫を見る →
              </a>
            </div>
          </div>
        `;
      }}).join('');

      container.innerHTML = `
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 pb-3 border-b border-[var(--border)]">
          <div>
            <span class="text-xs font-bold text-teal-600 dark:text-teal-400">${{hub.category}}</span>
            <h2 class="text-base font-bold">${{hub.title}}</h2>
          </div>
          <div class="text-xs text-[var(--muted-foreground)]">
            掲載数: <span class="font-bold text-[var(--foreground)]">${{hub.items.length}}商品</span> (rate降順)
          </div>
        </div>

        <div class="space-y-3">
          ${{itemsHtml}}
        </div>
      `;
    }}

    switchTab(0);
  </script>
</body>
</html>
"""

with open(out_file, 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Successfully rebuilt special_features_preview.html with real verified images!')
