import glob, re

with open('/tmp/article_styles.css', 'r', encoding='utf-8') as f:
    base_article_css = f.read()

# Unified Master Stylesheet for ALL articles (both pillar ranking & cluster articles)
MASTER_ARTICLE_CSS = f"""
  /* === Kurakaji Unified Master Article Stylesheet === */
{base_article_css}

  /* Responsive & Typography Harmonization */
  .article-container {{
    max-width: 880px;
    margin: 0 auto;
    padding: 2rem 1.25rem 5rem;
  }}
  .article-header-section, .article-header {{
    margin-bottom: 2.25rem;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 1.75rem;
  }}
  .category-tag, .article-tag {{
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: var(--radius-full);
    background-color: var(--color-brand-light);
    color: var(--color-brand-primary);
    font-size: 0.8rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
    border: 1px solid rgba(13, 148, 136, 0.25);
  }}
  .article-title, .article-h1 {{
    font-size: 1.9rem;
    font-weight: 800;
    line-height: 1.45;
    color: var(--color-text-main);
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
  }}
  .article-meta-info, .article-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 1.25rem;
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin-bottom: 1.25rem;
  }}
  .breadcrumb-trail, .breadcrumb-nav {{
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin-bottom: 1.5rem;
  }}
  .breadcrumb-trail ol {{
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    padding: 0;
    margin: 0;
  }}
  .breadcrumb-trail a, .breadcrumb-nav a {{
    color: var(--color-brand-primary);
    text-decoration: none;
    font-weight: 600;
  }}
  .breadcrumb-trail a:hover, .breadcrumb-nav a:hover {{
    text-decoration: underline;
  }}
  .breadcrumb-trail .sep, .breadcrumb-separator {{
    color: #94a3b8;
  }}
  .breadcrumb-trail .current {{
    color: #64748b;
  }}

  /* Guide Boxes & Content Cards */
  .guide-box {{
    background: #ffffff;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    margin: 2.5rem 0;
    box-shadow: var(--shadow-sm);
  }}
  .guide-box h2 {{
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 1.25rem;
    border-bottom: 2px solid var(--color-brand-primary);
    padding-bottom: 0.5rem;
    color: var(--color-text-main);
  }}
  .guide-box p {{
    font-size: 0.98rem;
    line-height: 1.8;
    color: #334155;
    margin-bottom: 1.2rem;
  }}

  /* Table styling */
  .comparison-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
  }}
  .comparison-table th, .comparison-table td {{
    padding: 12px;
    border: 1px solid var(--color-border);
    font-size: 0.9rem;
  }}

  /* Product Ranking Cards Responsive Fix */
  .ranking-card {{
    background: #ffffff;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 24px;
    margin-bottom: 35px;
    box-shadow: var(--shadow-sm);
  }}

  @media (max-width: 768px) {{
    .article-title, .article-h1 {{
      font-size: 1.45rem;
      line-height: 1.4;
    }}
    .article-container {{
      padding: 1.25rem 1rem 4rem;
    }}
    .guide-box {{
      padding: 1.25rem;
      margin: 1.5rem 0;
    }}
    .product-body {{
      flex-direction: column !important;
      align-items: center !important;
    }}
    .product-gallery {{
      width: 100% !important;
      max-width: 260px !important;
      margin: 0 auto 15px !important;
    }}
    .product-details {{
      width: 100% !important;
    }}
    .rank-header {{
      flex-direction: column;
      align-items: flex-start !important;
      gap: 10px;
    }}
    .price-tag {{
      align-self: flex-start;
    }}
    .product-item-card {{
      flex-direction: column !important;
      align-items: center;
      text-align: center;
    }}
    .pillar-cta-card {{
      padding: 1.25rem !important;
    }}
  }}
"""

all_files = glob.glob('articles/*.html') + glob.glob('articles/cluster/*.html')

for fpath in all_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace existing <style>...</style> or inject before </head>
    if '<style>' in html:
        html = re.sub(r'<style>.*?</style>', f"<style>\n{MASTER_ARTICLE_CSS}\n</style>", html, flags=re.DOTALL)
    else:
        html = html.replace('</head>', f"<style>\n{MASTER_ARTICLE_CSS}\n</style>\n</head>")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Applied unified master styles to: {fpath}")

print("All 10 articles fully harmonized with responsive design!")
