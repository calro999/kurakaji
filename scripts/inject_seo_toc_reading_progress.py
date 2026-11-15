import glob, re

TOC_PROGRESS_SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  // 1. Reading Progress Bar
  const progressBar = document.createElement('div');
  progressBar.id = 'reading-progress-bar';
  progressBar.style.cssText = 'position:fixed;top:0;left:0;height:4px;background:linear-gradient(90deg,#0d9488,#f59e0b);width:0%;z-index:99999;transition:width 0.1s ease-out;';
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', function() {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (window.pageYOffset / totalHeight) * 100;
    progressBar.style.width = Math.min(100, Math.max(0, progress)) + '%';
  });

  // 2. Auto Table of Contents Generator (if not already present)
  const container = document.querySelector('.article-container');
  if (container && !document.getElementById('auto-toc-box')) {
    const headings = container.querySelectorAll('h2');
    if (headings.length >= 3) {
      const tocBox = document.createElement('nav');
      tocBox.id = 'auto-toc-box';
      tocBox.style.cssText = 'background:#f8fafc;border:1.5px solid #e2e8f0;border-radius:14px;padding:20px 24px;margin:25px 0 35px;box-shadow:0 2px 8px rgba(0,0,0,0.03);';
      
      let tocHtml = '<div style="display:flex;align-items:center;justify-content:space-between;cursor:pointer;" id="toc-toggle-header">';
      tocHtml += '<span style="font-weight:800;font-size:1.05rem;color:#0f172a;display:flex;align-items:center;gap:8px;">📑 目次 [タップで開閉]</span>';
      tocHtml += '<span id="toc-arrow" style="font-size:0.85rem;color:#64748b;">▼</span></div>';
      tocHtml += '<ol id="toc-list" style="margin:14px 0 0;padding-left:22px;line-height:1.9;font-size:0.92rem;">';
      
      headings.forEach((h, idx) => {
        const id = h.id || 'section-' + (idx + 1);
        h.id = id;
        tocHtml += `<li><a href="#${id}" style="color:#0284c7;text-decoration:none;font-weight:600;">${h.textContent.trim()}</a></li>`;
      });
      tocHtml += '</ol>';
      tocBox.innerHTML = tocHtml;

      const lead = container.querySelector('.lead-box, .article-lead, .guide-box');
      if (lead) {
        lead.parentNode.insertBefore(tocBox, lead.nextSibling);
      } else {
        const header = container.querySelector('header');
        if (header) header.parentNode.insertBefore(tocBox, header.nextSibling);
      }

      // Toggle functionality
      const toggleHeader = document.getElementById('toc-toggle-header');
      const list = document.getElementById('toc-list');
      const arrow = document.getElementById('toc-arrow');
      toggleHeader.addEventListener('click', function() {
        if (list.style.display === 'none') {
          list.style.display = 'block';
          arrow.textContent = '▼';
        } else {
          list.style.display = 'none';
          arrow.textContent = '▲';
        }
      });
    }
  }
});
</script>
"""

files = glob.glob('articles/*.html') + glob.glob('articles/cluster/*.html')
for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'reading-progress-bar' not in c:
        c = c.replace('</body>', TOC_PROGRESS_SCRIPT + '\n</body>')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Added TOC & Reading Progress to {fpath}")

print("SEO UX & Dwell Time boosts injected into all articles!")
