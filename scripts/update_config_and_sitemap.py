import os, glob

base_dir = '/home/antigravity/kurakaji'
articles = sorted(glob.glob(os.path.join(base_dir, 'articles/**/*.html'), recursive=True))

# 1. Update vite.config.js
input_entries = [
    "        main: resolve(__dirname, 'index.html')",
    "        privacy: resolve(__dirname, 'privacy.html')",
    "        terms: resolve(__dirname, 'terms.html')",
    "        about: resolve(__dirname, 'about.html')"
]
for a in articles:
    rel_path = os.path.relpath(a, base_dir)
    var_name = rel_path.replace('articles/', '').replace('cluster/', 'cluster_').replace('.html', '').replace('-', '_')
    input_entries.append(f"        {var_name}: resolve(__dirname, '{rel_path}')")

vite_config_content = f"""import {{ defineConfig }} from 'vite';
import {{ resolve }} from 'path';

export default defineConfig({{
  server: {{
    port: 3000
  }},
  build: {{
    rollupOptions: {{
      input: {{
{','.join(input_entries)}
      }}
    }}
  }}
}});
"""

with open(os.path.join(base_dir, 'vite.config.js'), 'w', encoding='utf-8') as f:
    f.write(vite_config_content)

# 2. Update sitemap.xml
sitemap_urls = [
    """  <url>
    <loc>https://kurakaji.vercel.app/</loc>
    <lastmod>2026-11-12</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>""",
    """  <url>
    <loc>https://kurakaji.vercel.app/about.html</loc>
    <lastmod>2026-11-12</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>""",
    """  <url>
    <loc>https://kurakaji.vercel.app/terms.html</loc>
    <lastmod>2026-11-12</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.4</priority>
  </url>""",
    """  <url>
    <loc>https://kurakaji.vercel.app/privacy.html</loc>
    <lastmod>2026-11-12</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.4</priority>
  </url>"""
]

for a in articles:
    rel_path = os.path.relpath(a, base_dir)
    priority = "0.85" if "cluster" in rel_path else "0.9"
    sitemap_urls.append(f"""  <url>
    <loc>https://kurakaji.vercel.app/{rel_path}</loc>
    <lastmod>2026-11-12</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{priority}</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_urls)}
</urlset>
"""

with open(os.path.join(base_dir, 'public/sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_content)

print("vite.config.js & sitemap.xml updated with privacy, terms, about and all articles!")
