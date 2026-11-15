import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hero-section to remove search bar and focus purely on clean presentation
old_hero_pattern = re.compile(r'<section class="hero-section">.*?</section>', re.DOTALL)

new_hero = """<section class="hero-section">
    <div class="hero-inner">
      <div class="hero-pill">
        <span>2026年最新 QOL向上ギア</span>
      </div>
      <h1 class="hero-heading">
        暮らしをスマートにする、<br />厳選・小型＆生活家電カタログ
      </h1>
      <p class="hero-subtext">
        場所をとらず、日々の家事やデスクワークを快適に。<br />
        デザインと実用性、電気代のコスパをプロが検証した傑作小型家電のみをセレクト。
      </p>
    </div>
  </section>"""

html = old_hero_pattern.sub(new_hero, html, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Hero section redesigned without the redundant search bar!")
