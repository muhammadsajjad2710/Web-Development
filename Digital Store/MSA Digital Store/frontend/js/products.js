document.addEventListener('DOMContentLoaded', async () => {
  // Product detail page
  const detailRoot = document.getElementById('product-detail');
  if (detailRoot) {
    const id = new URLSearchParams(location.search).get('id');
    if (!id) {
      detailRoot.innerHTML = '<p class="loading">Product not found.</p>';
      return;
    }
    try {
      const p = await MSA.request(`/api/products/${id}`);
      const discount = p.original_price && p.original_price > p.price
        ? Math.round(((p.original_price - p.price) / p.original_price) * 100)
        : 0;
      const features = (p.features || '').split('\n').filter(Boolean);
      let qty = 1;
      detailRoot.innerHTML = `
        <nav class="muted" style="margin-bottom:1.25rem;font-size:0.8rem">
          <a href="index.html">Home</a> /
          <a href="products.html?category=${p.category?.slug || ''}">${p.category?.name || ''}</a> /
          <span>${p.name}</span>
        </nav>
        <div class="detail-grid">
          <div class="detail-image"><img src="${MSA.productImage(p)}" alt="${p.name}" /></div>
          <div>
            <span class="pill ${MSA.badgeClass(p.badge)}">${p.badge}</span>
            <h1 class="font-display" style="margin:0.75rem 0;font-size:1.8rem">${p.name}</h1>
            <div><span class="stars">${MSA.stars(p.rating)}</span> <span class="review-count">${p.rating} · ${p.review_count} reviews</span></div>
            <div class="price-row" style="margin:1rem 0">
              <span class="price" style="font-size:1.8rem">${MSA.formatPKR(p.price)}</span>
              ${p.original_price > p.price ? `<span class="old-price">${MSA.formatPKR(p.original_price)}</span><span class="pill pill-warehouse">Save ${discount}%</span>` : ''}
            </div>
            <div class="panel" style="margin-bottom:1rem">
              <strong>${p.seller?.business_name || 'Seller'}</strong>
              <div class="muted" style="font-size:0.82rem;margin-top:0.25rem">${p.seller?.is_verified ? 'Verified seller' : 'Marketplace seller'}</div>
            </div>
            <p class="muted">${p.description}</p>
            <ul>${features.map((f) => `<li style="margin:0.35rem 0">${f}</li>`).join('')}</ul>
            <p><strong>Stock:</strong> ${p.stock_status} · ${p.stock} units</p>
            <p class="muted">${p.delivery_info || ''}</p>
            <p class="muted">${p.return_policy || ''}</p>
            <div style="display:flex;flex-wrap:wrap;gap:0.75rem;margin-top:1.25rem;align-items:center">
              <div class="qty-box">
                <button type="button" id="qty-minus">−</button>
                <span id="qty-val">1</span>
                <button type="button" id="qty-plus">+</button>
              </div>
              <button class="btn btn-navy" id="btn-add" ${p.stock < 1 ? 'disabled' : ''}>Add to Cart</button>
              <button class="btn btn-teal" id="btn-buy" ${p.stock < 1 ? 'disabled' : ''}>Buy Now</button>
            </div>
          </div>
        </div>
        <section class="section" style="padding-left:0;padding-right:0">
          <h2 class="font-display">Related Products</h2>
          <div class="product-grid" id="related-grid" style="margin-top:1rem"></div>
        </section>`;

      document.getElementById('qty-minus').onclick = () => {
        qty = Math.max(1, qty - 1);
        document.getElementById('qty-val').textContent = qty;
      };
      document.getElementById('qty-plus').onclick = () => {
        qty = Math.min(p.stock || 1, qty + 1);
        document.getElementById('qty-val').textContent = qty;
      };
      document.getElementById('btn-add').onclick = () => MSA.addToCart(p, qty);
      document.getElementById('btn-buy').onclick = async () => {
        await MSA.addToCart(p, qty);
        location.href = 'checkout.html';
      };

      const related = await MSA.request(`/api/products?category=${p.category?.slug || ''}&limit=8`);
      const filtered = related.filter((r) => r.id !== p.id).slice(0, 4);
      const relatedGrid = document.getElementById('related-grid');
      relatedGrid.innerHTML = filtered.map((r) => MSA.productCardHTML(r)).join('');
      window.MSABindAddCart?.(relatedGrid, filtered);
    } catch (e) {
      detailRoot.innerHTML = `<p class="loading">${e.message}</p>`;
    }
  }

  // Listing page handled in same file when products-grid exists without detail
  const params = new URLSearchParams(location.search);
  const category = params.get('category') || '';
  const q = params.get('q') || '';
  const grid = document.getElementById('products-grid');
  const title = document.getElementById('listing-title');
  const countEl = document.getElementById('listing-count');
  const filters = document.getElementById('category-filters');
  const sortEl = document.getElementById('sort-select');

  if (!grid || detailRoot) return;

  try {
    const cats = await MSA.request('/api/categories');
    if (filters) {
      filters.innerHTML = `
        <li><button type="button" data-cat="" class="${!category ? 'active' : ''}">All Products</button></li>
        ${cats.map((c) => `
          <li><button type="button" data-cat="${c.slug}" class="${category === c.slug ? 'active' : ''}">${c.name}</button></li>
        `).join('')}`;
      filters.querySelectorAll('button').forEach((btn) => {
        btn.addEventListener('click', () => {
          const cat = btn.dataset.cat;
          const next = new URL(location.href);
          if (cat) next.searchParams.set('category', cat);
          else next.searchParams.delete('category');
          location.href = next.toString();
        });
      });
    }
    const active = cats.find((c) => c.slug === category);
    if (title) title.textContent = active ? active.name : (q ? `Results for “${q}”` : 'All Products');
  } catch (e) {
    if (filters) filters.innerHTML = `<li class="muted">${e.message}</li>`;
  }

  async function load() {
    grid.innerHTML = '<p class="loading">Loading products…</p>';
    const qs = new URLSearchParams();
    if (category) qs.set('category', category);
    if (q) qs.set('q', q);
    qs.set('limit', '50');
    try {
      let products = await MSA.request(`/api/products?${qs}`);
      const sort = sortEl?.value || 'featured';
      if (sort === 'price-asc') products = [...products].sort((a, b) => a.price - b.price);
      if (sort === 'price-desc') products = [...products].sort((a, b) => b.price - a.price);
      if (sort === 'rating') products = [...products].sort((a, b) => b.rating - a.rating);
      if (countEl) countEl.textContent = `${products.length} product${products.length !== 1 ? 's' : ''} available`;
      if (!products.length) {
        grid.innerHTML = '<p class="loading">No products match your filters.</p>';
        return;
      }
      grid.innerHTML = products.map((p) => MSA.productCardHTML(p)).join('');
      window.MSABindAddCart?.(grid, products);
    } catch (e) {
      grid.innerHTML = `<p class="loading">${e.message}</p>`;
    }
  }

  sortEl?.addEventListener('change', load);
  load();
});
