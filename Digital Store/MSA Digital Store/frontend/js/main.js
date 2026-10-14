/* Shared layout: header + footer + brand */
(function () {
  const categories = [
    ['Electronics', 'electronics'],
    ['Mobile Accessories', 'mobile-accessories'],
    ['Fashion', 'fashion'],
    ['Shoes', 'shoes'],
    ['Beauty Products', 'beauty-products'],
    ['Groceries', 'groceries'],
    ['Home & Kitchen', 'home-kitchen'],
    ['Baby Products', 'baby-products'],
    ['Books & Stationery', 'books-stationery'],
    ['Daily Use Items', 'daily-use-items'],
  ];

  const LOGO = 'images/Logo.png';

  function ensureFavicon() {
    if (document.querySelector('link[rel="icon"]')) return;
    const link = document.createElement('link');
    link.rel = 'icon';
    link.type = 'image/png';
    link.href = location.pathname.includes('/admin/') ? '../images/Logo.png' : LOGO;
    document.head.appendChild(link);
  }

  function headerHTML() {
    const auth = MSA.getToken();
    const loginLabel = auth ? (auth.full_name?.split(' ')[0] || 'Account') : 'Login';
    return `
    <div class="top-bar">Launching from Tehsil Quaidabad, District Khushab — <strong>Starting local. Scaling national. Reaching global.</strong></div>
    <header class="site-header">
      <div class="container header-inner">
        <a class="brand" href="index.html" aria-label="MSA Digital Store home">
          <img class="brand-logo" src="${LOGO}" alt="MSA Technologies" width="128" height="42" />
          <div class="brand-text">
            <strong>MSA Digital Store</strong>
            <span>By MSA Technologies</span>
          </div>
        </a>
        <form class="search-form" id="global-search" action="products.html" method="get">
          <input type="search" name="q" placeholder="Search products, categories, sellers..." aria-label="Search" />
        </form>
        <button class="mobile-toggle" id="mobile-toggle" type="button" aria-label="Menu">☰</button>
        <nav class="nav-actions" id="nav-actions">
          <button type="button" class="nav-btn" id="cat-toggle">Categories ▾</button>
          <a href="order-tracking.html">Track Order</a>
          <a href="seller-register.html">Become a Seller</a>
          <a href="login.html">${loginLabel}</a>
          ${auth?.role === 'admin' ? '<a href="admin/dashboard.html">Admin</a>' : ''}
          <a class="cart-btn" href="cart.html">Cart <span class="cart-count" data-cart-count>0</span></a>
        </nav>
      </div>
      <div class="container cat-panel" id="cat-panel">
        <div class="cat-grid">
          ${categories.map(([n, s]) => `<a href="products.html?category=${s}">${n}</a>`).join('')}
        </div>
      </div>
    </header>`;
  }

  function footerHTML() {
    return `
    <footer class="site-footer">
      <div class="container footer-grid">
        <div>
          <div class="brand" style="margin-bottom:1.1rem">
            <img class="brand-logo-footer" src="${LOGO}" alt="MSA Technologies" />
            <div class="brand-text">
              <strong>MSA Digital Store</strong>
              <span>By MSA Technologies</span>
            </div>
          </div>
          <p class="muted" style="color:rgba(255,255,255,0.58);line-height:1.55">Your trusted online shopping destination. A complete marketplace for customers, shops, and MSA Technologies products.</p>
          <p class="footer-vision">“Starting local. Scaling national. Reaching global.”</p>
        </div>
        <div>
          <h4>Quick Links</h4>
          <ul>
            <li><a href="index.html">About</a></li>
            <li><a href="seller-register.html">Become a Seller</a></li>
            <li><a href="order-tracking.html">Track Order</a></li>
            <li><a href="login.html">Login / Register</a></li>
          </ul>
        </div>
        <div>
          <h4>Policies</h4>
          <ul>
            <li><a href="#">Return Policy</a></li>
            <li><a href="#">Privacy Policy</a></li>
            <li><a href="#">Terms & Conditions</a></li>
            <li><a href="admin/login.html">Admin Login</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li>Tehsil Quaidabad, District Khushab, Pakistan</li>
            <li>+92 300 0000000</li>
            <li>support@msadigitalstore.pk</li>
          </ul>
        </div>
      </div>
      <div class="container footer-bottom">
        <span>© ${new Date().getFullYear()} MSA Digital Store by MSA Technologies. All rights reserved.</span>
        <span>Ready for WhatsApp automation, payments, courier & mobile app.</span>
      </div>
    </footer>`;
  }

  document.addEventListener('DOMContentLoaded', () => {
    ensureFavicon();
    const mountHeader = document.getElementById('site-header-mount');
    const mountFooter = document.getElementById('site-footer-mount');
    if (mountHeader) mountHeader.innerHTML = headerHTML();
    if (mountFooter) mountFooter.innerHTML = footerHTML();

    document.getElementById('cat-toggle')?.addEventListener('click', () => {
      document.getElementById('cat-panel')?.classList.toggle('open');
    });
    document.getElementById('mobile-toggle')?.addEventListener('click', () => {
      document.getElementById('nav-actions')?.classList.toggle('open');
    });

    MSA.updateCartBadge();

    const homeGrid = document.getElementById('home-products');
    if (homeGrid) {
      MSA.request('/api/products?limit=8')
        .then((products) => {
          homeGrid.innerHTML = products.map((p) => MSA.productCardHTML(p)).join('');
          bindAddCart(homeGrid, products);
        })
        .catch((e) => {
          homeGrid.innerHTML = `<p class="loading">${e.message}. Is the API running?</p>`;
        });
    }

    const catMount = document.getElementById('home-categories');
    if (catMount) {
      MSA.request('/api/categories')
        .then((cats) => {
          const icons = {
            electronics: '⚡',
            'mobile-accessories': '📱',
            fashion: '👔',
            shoes: '👟',
            'beauty-products': '✨',
            groceries: '🛒',
            'home-kitchen': '🏠',
            'baby-products': '🍼',
            'books-stationery': '📚',
            'daily-use-items': '🧰',
          };
          catMount.innerHTML = cats.map((c) => `
            <a class="category-card" href="products.html?category=${c.slug}">
              <div class="cat-icon">${icons[c.slug] || '📦'}</div>
              <h3>${c.name}</h3>
              <p>${c.description || ''}</p>
            </a>`).join('');
        })
        .catch(() => {});
    }
  });

  function bindAddCart(container, products) {
    container.querySelectorAll('[data-add-cart]').forEach((btn) => {
      btn.addEventListener('click', async () => {
        const id = Number(btn.getAttribute('data-add-cart'));
        const product = products.find((p) => p.id === id);
        if (product) await MSA.addToCart(product);
      });
    });
  }

  window.MSABindAddCart = bindAddCart;
})();
