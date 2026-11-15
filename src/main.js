import { CATEGORIES, INITIAL_ITEMS } from './data.js';

let currentCategory = 'all';
let currentSort = 'standard';
let currentSearchQuery = '';
let itemsList = [...INITIAL_ITEMS];
let isLoading = false;

// DOM Elements
const productsGrid = document.getElementById('products-grid');
const categoryScroll = document.getElementById('category-scroll');
const searchForm = document.getElementById('search-form');
const searchInput = document.getElementById('search-input');
const sortSelect = document.getElementById('sort-select');
const quickTags = document.getElementById('quick-tags');
const activeCategoryName = document.getElementById('active-category-name');
const itemCountBadge = document.getElementById('item-count-badge');

// Initialize
export function initApp() {
  renderCategories();
  renderProducts();
  setupEventListeners();
}

// Render Category Filter Tabs
function renderCategories() {
  categoryScroll.innerHTML = CATEGORIES.map(cat => `
    <button class="category-tab-btn ${cat.id === currentCategory ? 'active' : ''}" data-cat="${cat.id}">
      <span>${cat.name}</span>
    </button>
  `).join('');
}

// Fetch products from Rakuten API or fallback to curated list
async function fetchProducts(query = '', categoryId = 'all') {
  isLoading = true;
  productsGrid.innerHTML = `
    <div style="grid-column: 1/-1; text-align: center; padding: 3rem 1rem;">
      <div style="display: inline-block; width: 36px; height: 36px; border: 3px solid #e2e8f0; border-top-color: var(--color-brand-primary); border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
      <p style="margin-top: 1rem; color: var(--color-text-muted); font-size: 0.9rem;">最新の商品情報を楽天APIから読み込み中...</p>
    </div>
    <style>@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }</style>
  `;

  try {
    let targetKeyword = query;
    if (!targetKeyword) {
      const catObj = CATEGORIES.find(c => c.id === categoryId);
      targetKeyword = catObj ? catObj.query : '小型家電 暮らし 便利';
    }

    const sortParam = currentSort;
    const res = await fetch(`/api/items?keyword=${encodeURIComponent(targetKeyword)}&sort=${sortParam}&hits=30`);
    
    if (res.ok) {
      const data = await res.json();
      if (data.items && data.items.length > 0) {
        itemsList = data.items.map(item => ({
          ...item,
          tagline: item.itemCaption ? item.itemCaption.substring(0, 50) + '...' : '日常の快適さを高める厳選小型家電',
          categoryLabel: getCategoryLabel(categoryId),
          badge: item.reviewAverage >= 4.5 ? '高評価' : '人気'
        }));
      } else {
        itemsList = INITIAL_ITEMS;
      }
    } else {
      // Fallback
      fallbackFilter(query, categoryId);
    }
  } catch (err) {
    console.warn('API error, using curated items:', err);
    fallbackFilter(query, categoryId);
  } finally {
    isLoading = false;
    renderProducts();
  }
}

function fallbackFilter(query, categoryId) {
  let list = [...INITIAL_ITEMS];
  if (categoryId !== 'all') {
    list = list.filter(item => item.category === categoryId);
  }
  if (query) {
    const q = query.toLowerCase();
    list = list.filter(item => 
      item.title.toLowerCase().includes(q) || 
      (item.tagline && item.tagline.toLowerCase().includes(q))
    );
  }
  itemsList = list;
}

function getCategoryLabel(catId) {
  const cat = CATEGORIES.find(c => c.id === catId);
  return cat ? cat.name : '小型家電';
}

// Render Products Grid
function renderProducts() {
  const currentCatObj = CATEGORIES.find(c => c.id === currentCategory);
  if (activeCategoryName) {
    activeCategoryName.textContent = currentSearchQuery 
      ? `「${currentSearchQuery}」の検索結果` 
      : (currentCatObj ? currentCatObj.name : '全商品');
  }
  if (itemCountBadge) {
    itemCountBadge.textContent = `${itemsList.length} 件`;
  }

  if (itemsList.length === 0) {
    productsGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 4rem 1rem; background: #fff; border-radius: var(--radius-lg); border: 1px dashed var(--color-border);">
        <p style="font-size: 1.1rem; font-weight: 700; color: var(--color-text-main); margin-bottom: 0.5rem;">条件に一致する家電が見つかりませんでした</p>
        <p style="color: var(--color-text-muted); font-size: 0.9rem;">別のキーワードで検索するか、カテゴリーを変更してみてください。</p>
        <button id="reset-filter-btn" style="margin-top: 1.25rem; padding: 0.6rem 1.4rem; background: var(--color-brand-primary); color: #fff; border-radius: var(--radius-full); font-weight: 600; font-size: 0.85rem;">全商品を表示する</button>
      </div>
    `;
    document.getElementById('reset-filter-btn')?.addEventListener('click', () => {
      currentCategory = 'all';
      currentSearchQuery = '';
      if (searchInput) searchInput.value = '';
      renderCategories();
      fetchProducts('', 'all');
    });
    return;
  }

  productsGrid.innerHTML = itemsList.map((item, idx) => {
    const images = item.images && item.images.length > 0 ? item.images : [item.imageUrl];
    const itemDomId = `item-card-${idx}`;
    return `
    <article class="product-card" id="${itemDomId}">
      <a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" class="card-media-wrap" style="display:block; text-decoration:none;">
        ${item.badge ? `<span class="badge-pill ${item.badge === '人気No.1' ? 'hot' : ''}">${item.badge}</span>` : ''}
        <img 
          class="card-img" 
          id="${itemDomId}-main-img"
          src="${images[0]}" 
          alt="${item.title}" 
          loading="lazy"
        />
      </a>

      ${images.length > 1 ? `
        <div class="card-thumbs-bar">
          ${images.map((img, imgIdx) => `
            <button 
              type="button" 
              class="thumb-dot-btn ${imgIdx === 0 ? 'active' : ''}" 
              data-card-id="${itemDomId}"
              data-src="${img}"
              title="画像 ${imgIdx + 1}"
            >
              <img src="${img}" alt="" />
            </button>
          `).join('')}
        </div>
      ` : ''}

      <div class="card-body">
        <span class="card-category-tag">${item.categoryLabel || '厳選小型家電'}</span>
        <h3 class="card-title">
          <a href="${item.affiliateUrl}" target="_blank" rel="noopener noreferrer nofollow" class="card-title-link">
            <span class="card-brand-label">${item.title.includes(' | ') ? item.title.split(' | ')[0] : '人気モデル'}</span>
            <span class="card-name-label">${item.title.includes(' | ') ? item.title.split(' | ')[1] : item.title}</span>
          </a>
        </h3>
        <p class="card-tagline">${item.tagline || ''}</p>
        
        ${item.features && item.features.length > 0 ? `
          <ul class="card-features">
            ${item.features.slice(0, 3).map(f => `<li>${f}</li>`).join('')}
          </ul>
        ` : ''}

        <div class="card-footer">
          <div class="shop-name-row">
            <span class="shop-badge">取扱店</span>
            <span class="shop-title" title="${item.shopName || '楽天市場'}">${item.shopName || '楽天市場'}</span>
          </div>
          <div class="price-row">
            <span class="price-label">参考価格（税込）</span>
            <span class="price-num">${item.priceFormatted || Number(item.price).toLocaleString() + '円'}</span>
          </div>
          <a 
            href="${item.affiliateUrl}" 
            target="_blank" 
            rel="noopener noreferrer nofollow" 
            class="card-cta-btn"
          >
            楽天市場で詳細・在庫を見る <span>→</span>
          </a>
        </div>
      </div>
    </article>
  `}).join('');

  // Attach thumbnail click handlers
  productsGrid.querySelectorAll('.thumb-dot-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const cardId = btn.dataset.cardId;
      const targetSrc = btn.dataset.src;
      const mainImg = document.getElementById(`${cardId}-main-img`);
      if (mainImg) {
        mainImg.src = targetSrc;
      }
      btn.closest('.card-thumbs-bar').querySelectorAll('.thumb-dot-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });
}

// Setup Event Listeners
function setupEventListeners() {
  // Category switching
  categoryScroll.addEventListener('click', (e) => {
    const btn = e.target.closest('.category-tab-btn');
    if (!btn) return;
    const catId = btn.dataset.cat;
    if (catId === currentCategory) return;
    
    currentCategory = catId;
    currentSearchQuery = '';
    if (searchInput) searchInput.value = '';
    renderCategories();
    fetchProducts('', currentCategory);
  });

  // Search input submission (if present)
  if (searchForm && searchInput) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = searchInput.value.trim();
      currentSearchQuery = q;
      fetchProducts(q, currentCategory);
    });
  }

  // Quick tag pills
  if (quickTags) {
    quickTags.addEventListener('click', (e) => {
      const btn = e.target.closest('.quick-tag-btn');
      if (!btn) return;
      const tagQuery = btn.dataset.query || btn.textContent.replace('#', '').trim();
      searchInput.value = tagQuery;
      currentSearchQuery = tagQuery;
      fetchProducts(tagQuery, currentCategory);
    });
  }

  // Sorting
  sortSelect.addEventListener('change', (e) => {
    currentSort = e.target.value;
    if (currentSort === 'priceAsc') {
      itemsList.sort((a, b) => a.price - b.price);
      renderProducts();
    } else if (currentSort === 'priceDesc') {
      itemsList.sort((a, b) => b.price - a.price);
      renderProducts();
    } else {
      fetchProducts(currentSearchQuery, currentCategory);
    }
  });
}
