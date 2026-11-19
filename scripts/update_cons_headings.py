import glob, re, os

new_heading = "<h5>購入前に知っておきたいポイント</h5>"
old_heading = "<h5>気になる不安・疑問をプロが先回り解消</h5>"

files = sorted(glob.glob('articles/*.html'))
total_updated = 0

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    if old_heading in content:
        count = content.count(old_heading)
        content = content.replace(old_heading, new_heading)
        with open(fpath, 'w', encoding='utf-8') as fp:
            fp.write(content)
        total_updated += count
        print(f"Updated {count} in {os.path.basename(fpath)}")

print(f"\nTotal updated in articles: {total_updated}")

# Also update scripts/feature_updater.py
updater_file = 'scripts/feature_updater.py'
if os.path.exists(updater_file):
    with open(updater_file, 'r', encoding='utf-8') as fp:
        u_content = fp.read()
    if old_heading in u_content:
        u_content = u_content.replace(old_heading, new_heading)
        with open(updater_file, 'w', encoding='utf-8') as fp:
            fp.write(u_content)
        print("Updated scripts/feature_updater.py template")

print("Done.")
