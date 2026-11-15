import os, glob

BASE_DIR = '/home/antigravity/kurakaji'
all_html = glob.glob(os.path.join(BASE_DIR, '**/*.html'), recursive=True)
all_html = [f for f in all_html if 'node_modules' not in f and 'dist' not in f]

gtm_tag = """  <!-- Google Tag Manager / Analytics -->
  <script async src="https://www.googletagmanager.com/gtm.js?id=GTM-P33SX8W6"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
  </script>
</head>"""

count = 0
for fpath in all_html:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'GTM-P33SX8W6' in content:
        continue

    if '</head>' in content:
        # replace </head> with gtm_tag
        new_content = content.replace('</head>', gtm_tag, 1)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Successfully injected GTM/Analytics tag into {count} HTML files!")
