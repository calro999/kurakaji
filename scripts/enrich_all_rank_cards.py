import re, glob, os

files = [
    'articles/compact-air-fryer-best7.html',
    'articles/compact-ceramic-heater-best7.html',
    'articles/compact-coffee-maker-best7.html',
    'articles/compact-desk-cooler-fan-best7.html',
    'articles/compact-electric-blanket-best7.html',
    'articles/compact-electric-pressure-cooker-best7.html',
    'articles/compact-electric-snow-blower-best7.html',
    'articles/compact-futon-dryer-best10.html',
    'articles/compact-shoe-dryer-best7.html',
    'articles/compact-window-radiator-best7.html',
    'articles/desk-panel-heater-best10.html',
    'articles/futon-vacuum-cleaner-best7.html',
    'articles/large-room-heater-best10.html',
    'articles/multifunction-cooker-compact-best7.html',
    'articles/single-person-kotatsu-heater-best10.html',
    'articles/wearable-blanket-rechargeable-warmer-best10.html',
    'articles/november-clothes-dryer-dehumidifier.html',
    'articles/november-compact-kotatsu-warmth.html',
    'articles/november-electric-blanket-carpet.html',
    'articles/november-humidifier-dryness-prevention.html',
    'articles/november-winter-heating-super-guide.html'
]

# In these files, replace <div class="cons-box">...</div> header from
# '購入前に確認したい注意点（デメリット）' to '購入前の不安・疑問を解消（Q&A検証）'
# or soften and resolve them so they read like reassuring concern-solvers.
for fpath in files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r', encoding='utf-8') as fp:
        html = fp.read()
    
    # Change the cons-box header to focus on proactive resolution
    old_header = r'<h5>購入前に確認したい注意点（デメリット）</h5>'
    new_header = r'<h5>気になる不安・疑問をプロが先回り解消</h5>'
    html = re.sub(old_header, new_header, html)
    
    with open(fpath, 'w', encoding='utf-8') as fp:
        fp.write(html)
    print(f"Updated header in {fpath}")

print("All cons-box headers updated.")
