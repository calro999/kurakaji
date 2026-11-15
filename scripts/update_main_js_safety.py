with open('src/main.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Guard searchInput and searchForm
text = text.replace(
    "searchInput.value = '';",
    "if (searchInput) searchInput.value = '';"
)

old_search_listener = """  // Search input submission
  searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const q = searchInput.value.trim();
    currentSearchQuery = q;
    fetchProducts(q, currentCategory);
  });"""

new_search_listener = """  // Search input submission (if present)
  if (searchForm && searchInput) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = searchInput.value.trim();
      currentSearchQuery = q;
      fetchProducts(q, currentCategory);
    });
  }"""

text = text.replace(old_search_listener, new_search_listener)

with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Guarded search listeners in src/main.js!")
