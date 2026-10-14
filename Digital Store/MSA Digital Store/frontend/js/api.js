/* MSA Digital Store — API & shared utilities */
const API_BASE = window.location.origin.includes('5500') || window.location.protocol === 'file:'
  ? 'http://127.0.0.1:8000'
  : '';

const MSA = {
  apiBase: API_BASE,

  getToken() {
    try { return JSON.parse(localStorage.getItem('msa_auth') || 'null'); } catch { return null; }
  },

  setAuth(data) {
    localStorage.setItem('msa_auth', JSON.stringify(data));
  },

  clearAuth() {
    localStorage.removeItem('msa_auth');
  },

  isLoggedIn() {
    return !!this.getToken()?.access_token;
  },

  authHeaders() {
    const auth = this.getToken();
    return auth?.access_token ? { Authorization: `Bearer ${auth.access_token}` } : {};
  },

  async request(path, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...this.authHeaders(),
      ...(options.headers || {}),
    };
    const res = await fetch(`${this.apiBase}${path}`, { ...options, headers });
    let data = null;
    const text = await res.text();
    try { data = text ? JSON.parse(text) : null; } catch { data = { detail: text }; }
    if (!res.ok) {
      const detail = data?.detail;
      const msg = Array.isArray(detail)
        ? detail.map((d) => d.msg || JSON.stringify(d)).join(', ')
        : (detail || data?.message || `Request failed (${res.status})`);
      const err = new Error(msg);
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  },

  // Guest cart in localStorage
  getGuestCart() {
    try { return JSON.parse(localStorage.getItem('msa_guest_cart') || '[]'); } catch { return []; }
  },

  setGuestCart(items) {
    localStorage.setItem('msa_guest_cart', JSON.stringify(items));
    this.updateCartBadge();
  },

  addGuestCart(product, qty = 1) {
    const items = this.getGuestCart();
    const existing = items.find((i) => i.product_id === product.id);
    if (existing) existing.quantity += qty;
    else {
      items.push({
        product_id: product.id,
        quantity: qty,
        name: product.name,
        price: product.price,
        image: product.images?.[0]?.url || '',
        seller: product.seller?.business_name || '',
        stock: product.stock,
      });
    }
    this.setGuestCart(items);
  },

  guestCartCount() {
    return this.getGuestCart().reduce((s, i) => s + i.quantity, 0);
  },

  async updateCartBadge() {
    const el = document.querySelectorAll('[data-cart-count]');
    let count = this.guestCartCount();
    const auth = this.getToken();
    if (auth?.role === 'customer' && auth.access_token) {
      try {
        const cart = await this.request('/api/cart/me');
        count = cart.item_count || 0;
      } catch { /* keep guest count */ }
    }
    el.forEach((node) => {
      node.textContent = count;
      node.style.display = count > 0 ? 'grid' : 'none';
    });
  },

  formatPKR(amount) {
    return `PKR ${Number(amount || 0).toLocaleString('en-PK')}`;
  },

  stars(rating) {
    const full = Math.round(Number(rating) || 0);
    return '★'.repeat(Math.min(5, full)) + '☆'.repeat(Math.max(0, 5 - full));
  },

  badgeClass(badge) {
    if (badge === 'MSA Product') return 'pill-msa';
    if (badge === 'Warehouse Available') return 'pill-warehouse';
    return 'pill-verified';
  },

  productImage(product) {
    return product.images?.find((i) => i.is_primary)?.url
      || product.images?.[0]?.url
      || `https://picsum.photos/seed/msa${product.id}/600/600`;
  },

  toast(message, type = 'success') {
    let wrap = document.querySelector('.toast-wrap');
    if (!wrap) {
      wrap = document.createElement('div');
      wrap.className = 'toast-wrap';
      document.body.appendChild(wrap);
    }
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.textContent = message;
    wrap.appendChild(t);
    setTimeout(() => t.remove(), 3200);
  },

  async addToCart(product, qty = 1) {
    if (product.stock_status === 'out-of-stock' || product.stock < 1) {
      this.toast('Product is out of stock', 'error');
      return;
    }
    const auth = this.getToken();
    if (auth?.role === 'customer' && auth.access_token) {
      try {
        await this.request('/api/cart/add', {
          method: 'POST',
          body: JSON.stringify({ product_id: product.id, quantity: qty }),
        });
        this.toast('Added to cart');
        await this.updateCartBadge();
        return;
      } catch (e) {
        this.toast(e.message, 'error');
        return;
      }
    }
    this.addGuestCart(product, qty);
    this.toast('Added to cart');
  },

  productCardHTML(p) {
    const discount = p.original_price && p.original_price > p.price
      ? Math.round(((p.original_price - p.price) / p.original_price) * 100)
      : 0;
    const oos = p.stock_status === 'out-of-stock';
    return `
      <article class="product-card">
        <a class="product-image" href="product-detail.html?id=${p.id}">
          <img src="${this.productImage(p)}" alt="${p.name}" loading="lazy" />
          <div class="card-badges">
            <span class="pill ${this.badgeClass(p.badge)}">${p.badge}</span>
            ${discount ? `<span class="pill pill-sale">-${discount}%</span>` : ''}
          </div>
          ${oos ? '<div class="pill-oos">Out of Stock</div>' : ''}
          ${p.stock_status === 'low-stock' && !oos ? '<span class="pill pill-low" style="position:absolute;bottom:0.75rem;left:0.75rem">Low Stock</span>' : ''}
        </a>
        <div class="product-body">
          <div class="product-cat">${p.category?.name || ''}</div>
          <h3><a href="product-detail.html?id=${p.id}">${p.name}</a></h3>
          <div><span class="stars">${this.stars(p.rating)}</span> <span class="review-count">(${p.review_count})</span></div>
          <p class="seller-line">Sold by <strong>${p.seller?.business_name || 'Seller'}</strong></p>
          <div class="price-row">
            <span class="price">${this.formatPKR(p.price)}</span>
            ${p.original_price > p.price ? `<span class="old-price">${this.formatPKR(p.original_price)}</span>` : ''}
          </div>
          <div class="card-actions">
            <button class="btn btn-primary" ${oos ? 'disabled' : ''} data-add-cart="${p.id}">Add to Cart</button>
            <a class="btn btn-outline-dark" href="product-detail.html?id=${p.id}">View</a>
          </div>
        </div>
      </article>`;
  },
};

window.MSA = MSA;
