import re, glob

with open('/tmp/article_styles.css', 'r', encoding='utf-8') as f:
    article_css = f.read()

# Additional cluster specific responsive styles
cluster_extra_css = """
  /* Cluster Article Polished Theme */
  .article-container {
    max-width: 860px;
    margin: 0 auto;
    padding: 2rem 1.25rem 5rem;
  }
  .article-header-section {
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 1.5rem;
  }
  .category-tag {
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: var(--radius-full);
    background-color: #f0fdf4;
    color: #16a34a;
    font-size: 0.8rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
    border: 1px solid #bbf7d0;
  }
  .article-title {
    font-size: 1.85rem;
    font-weight: 800;
    line-height: 1.45;
    color: var(--color-text-main);
    margin-bottom: 1rem;
  }
  .article-meta-info {
    display: flex;
    flex-wrap: wrap;
    gap: 1.25rem;
    font-size: 0.85rem;
    color: var(--color-text-muted);
  }
  .breadcrumb-trail {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    margin-bottom: 1.5rem;
  }
  .breadcrumb-trail ol {
    list-style: none;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    padding: 0;
    margin: 0;
  }
  .breadcrumb-trail a {
    color: var(--color-brand-primary);
    text-decoration: none;
    font-weight: 600;
  }
  .breadcrumb-trail .sep {
    color: #94a3b8;
  }
  .breadcrumb-trail .current {
    color: #64748b;
  }
  .guide-box {
    background: #ffffff;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    margin: 2.5rem 0;
    box-shadow: var(--shadow-sm);
  }
  .guide-box h2 {
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 1.2rem;
    border-bottom: 2px solid var(--color-brand-primary);
    padding-bottom: 0.5rem;
    color: var(--color-text-main);
  }
  .guide-box p {
    font-size: 0.98rem;
    line-height: 1.8;
    color: #334155;
    margin-bottom: 1.2rem;
  }
  .comparison-table th, .comparison-table td {
    font-size: 0.9rem;
    line-height: 1.5;
  }
  @media (max-width: 640px) {
    .article-title {
      font-size: 1.45rem;
    }
    .guide-box {
      padding: 1.25rem;
      margin: 1.5rem 0;
    }
    .product-item-card {
      flex-direction: column !important;
      align-items: center;
      text-align: center;
    }
  }
"""

cluster_files = glob.glob('articles/cluster/*.html')

for cf in cluster_files:
    with open(cf, 'r', encoding='utf-8') as f:
        content = f.read()

    # If <style> doesn't already contain article_container styling
    if '.article-container' not in content:
        style_block = f"<style>\n{article_css}\n{cluster_extra_css}\n</style>\n</head>"
        content = content.replace('</head>', style_block)
        with open(cf, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected complete responsive design stylesheet into {cf}")
    else:
        print(f"{cf} already has styles, updating...")

print("Cluster articles design fixed!")
