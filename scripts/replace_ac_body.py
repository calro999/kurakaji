with open("articles/cluster/ac-keep-on-vs-off-electricity-test.html", "r", encoding="utf-8") as f:
    c = f.read()

# Locate from the second </header> to the start of FAQ box
h2_idx = c.find("</header>", 21400)
faq_idx = c.find("<!-- FAQ Section -->")
if faq_idx == -1:
    faq_idx = c.find("よくある質問（FAQ）")
    faq_idx = c.rfind("<div", 0, faq_idx)

print(f"h2_idx: {h2_idx}, faq_idx: {faq_idx}")

# Read the rich body
from deep_enrich_ac_article import rich_body

new_content = c[:h2_idx+9] + "\n\n" + rich_body.strip() + "\n\n    " + c[faq_idx:]

with open("articles/cluster/ac-keep-on-vs-off-electricity-test.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replacement complete!")
