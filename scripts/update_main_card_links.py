with open('src/main.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Make card image clickable
old_media = '''      <div class="card-media-wrap">
        ${item.badge ? `<span class="badge-pill ${item.badge === '人気No.1' ? 'hot' : ''}">${item.badge}</span>` : ''}
        <img 
          class="card-img" 
          id="${itemDomId}-main-img"
          src="${images[0]}" 
          alt="${item.title}" 
          loading="lazy"
        />
      </div>'''

new_media = '''      <a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" class="card-media-wrap" style="display:block; text-decoration:none;">
        ${item.badge ? `<span class="badge-pill ${item.badge === '人気No.1' ? 'hot' : ''}">${item.badge}</span>` : ''}
        <img 
          class="card-img" 
          id="${itemDomId}-main-img"
          src="${images[0]}" 
          alt="${item.title}" 
          loading="lazy"
        />
      </a>'''

# Make card title clickable
old_title = '''<h3 class="card-title" title="${item.title}">${item.title}</h3>'''
new_title = '''<h3 class="card-title" title="${item.title}"><a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" style="color:inherit; text-decoration:none;">${item.title}</a></h3>'''

assert old_media in c, "old_media not found"
assert old_title in c, "old_title not found"

c = c.replace(old_media, new_media, 1)
c = c.replace(old_title, new_title, 1)

with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("src/main.js updated with clickable image and title links!")
