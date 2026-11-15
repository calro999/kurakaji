with open('src/main.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's inspect the title rendering in card-body:
# We want:
# <h3 class="card-title">
#   <a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" class="card-title-link">
#     <span class="card-brand">${brand}</span>
#     <span class="card-name">${name}</span>
#   </a>
# </h3>

old_title_snippet = '<h3 class="card-title" title="${item.title}"><a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" style="color:inherit; text-decoration:none;">${item.title}</a></h3>'

new_title_snippet = '''<h3 class="card-title">
          <a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" class="card-title-link">
            <span class="card-brand-label">${item.title.includes(' | ') ? item.title.split(' | ')[0] : '人気モデル'}</span>
            <span class="card-name-label">${item.title.includes(' | ') ? item.title.split(' | ')[1] : item.title}</span>
          </a>
        </h3>'''

assert old_title_snippet in c, "old_title_snippet not found"
c = c.replace(old_title_snippet, new_title_snippet, 1)

# Also ensure tagline doesn't strip <br /> or truncate
with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("src/main.js updated with 2-line structured brand/name rendering!")
