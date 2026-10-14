(function () {
  const path = location.pathname;
  function requireAdmin() {
    const auth = MSA.getToken();
    if (!auth?.access_token || auth.role !== 'admin') {
      location.href = 'login.html';
      return false;
    }
    return true;
  }

  function sidebar(active) {
    const links = [
      ['dashboard.html', 'Dashboard'],
      ['products.html', 'Products'],
      ['orders.html', 'Orders'],
      ['inventory.html', 'Inventory'],
      ['sellers.html', 'Sellers'],
      ['reports.html', 'Reports'],
    ];
    return `
      <aside class="admin-sidebar" id="admin-sidebar">
        <div class="admin-brand">
          <img src="../images/Logo.png" alt="MSA" style="height:36px;width:auto;background:#fff;border-radius:8px;padding:0.25rem 0.4rem;object-fit:contain" />
          <div>
            <strong style="font-family:var(--display);font-size:0.9rem">Admin Dashboard</strong>
            <div style="font-size:0.65rem;color:rgba(158,193,255,0.95);text-transform:uppercase;letter-spacing:0.06em">MSA Digital Store</div>
          </div>
        </div>
        <nav class="admin-nav">
          ${links.map(([href, label]) => `<a href="${href}" class="${active === href ? 'active' : ''}">${label}</a>`).join('')}
          <a href="../index.html">← Storefront</a>
          <a href="#" id="admin-logout">Logout</a>
        </nav>
        <div style="padding:1rem;font-size:0.68rem;color:rgba(255,255,255,0.4);border-top:1px solid #122744">
          Future-ready: WhatsApp, payments, courier & mobile app
        </div>
      </aside>`;
  }

  document.addEventListener('DOMContentLoaded', async () => {
    // Admin login page
    const loginForm = document.getElementById('admin-login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msg = document.getElementById('admin-login-msg');
        try {
          const data = await MSA.request('/api/auth/admin/login', {
            method: 'POST',
            body: JSON.stringify({
              email: loginForm.email.value.trim(),
              password: loginForm.password.value,
            }),
          });
          MSA.setAuth(data);
          location.href = 'dashboard.html';
        } catch (err) {
          msg.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
        }
      });
      return;
    }

    if (!requireAdmin()) return;

    const shell = document.getElementById('admin-shell');
    const page = document.body.dataset.page || 'dashboard.html';
    if (shell && !shell.dataset.ready) {
      const content = shell.innerHTML;
      shell.innerHTML = sidebar(page) + `<div class="admin-main">
        <div class="admin-top">
          <div style="display:flex;gap:0.6rem;align-items:center">
            <button type="button" class="mobile-admin-btn" id="sidebar-toggle">☰</button>
            <div>
              <h1 id="admin-title">Admin</h1>
              <div style="font-size:0.75rem;color:rgba(11,29,54,0.55)">MSA Digital Store operations</div>
            </div>
          </div>
          <div style="font-size:0.85rem">${MSA.getToken()?.full_name || 'Admin'}</div>
        </div>
        <div class="admin-content">${content}</div>
      </div>`;
      shell.dataset.ready = '1';
      document.getElementById('sidebar-toggle')?.addEventListener('click', () => {
        document.getElementById('admin-sidebar')?.classList.toggle('open');
      });
      document.getElementById('admin-logout')?.addEventListener('click', (e) => {
        e.preventDefault();
        MSA.clearAuth();
        location.href = 'login.html';
      });
    }

    if (page === 'dashboard.html') await loadDashboard();
    if (page === 'products.html') await loadProducts();
    if (page === 'orders.html') await loadOrders();
    if (page === 'inventory.html') await loadInventory();
    if (page === 'sellers.html') await loadSellers();
    if (page === 'reports.html') await loadReports();
  });

  async function loadDashboard() {
    document.getElementById('admin-title').textContent = 'Dashboard';
    const stats = await MSA.request('/api/admin/dashboard');
    document.getElementById('dash-stats').innerHTML = `
      <div class="stat-card"><div class="label">Total Orders</div><div class="value">${stats.total_orders}</div></div>
      <div class="stat-card gold"><div class="label">Total Sales</div><div class="value">${MSA.formatPKR(stats.total_sales)}</div></div>
      <div class="stat-card"><div class="label">Total Products</div><div class="value">${stats.total_products}</div></div>
      <div class="stat-card"><div class="label">Total Customers</div><div class="value">${stats.total_customers}</div></div>
      <div class="stat-card"><div class="label">Active Sellers</div><div class="value">${stats.active_sellers}</div></div>
      <div class="stat-card amber"><div class="label">Low Stock</div><div class="value">${stats.low_stock_products}</div></div>
      <div class="stat-card gold"><div class="label">Pending Orders</div><div class="value">${stats.pending_orders}</div></div>
      <div class="stat-card amber"><div class="label">Returned</div><div class="value">${stats.returned_orders}</div></div>`;

    document.getElementById('recent-orders').innerHTML = `
      <div class="panel-head"><h2>Recent Orders</h2></div>
      <table>
        <thead><tr><th>Order</th><th>Customer</th><th>Total</th><th>Status</th></tr></thead>
        <tbody>
          ${(stats.recent_orders || []).map((o) => `
            <tr><td>${o.order_number}</td><td>${o.customer_name}</td><td>${MSA.formatPKR(o.total_amount)}</td><td>${o.status}</td></tr>
          `).join('') || '<tr><td colspan="4">No orders yet</td></tr>'}
        </tbody>
      </table>`;

    document.getElementById('top-products').innerHTML = `
      <div class="panel-head"><h2>Top Selling Products</h2></div>
      <table>
        <thead><tr><th>Product</th><th>Sold</th><th>Revenue</th></tr></thead>
        <tbody>
          ${(stats.top_selling_products || []).map((p) => `
            <tr><td>${p.name}</td><td>${p.sold}</td><td>${MSA.formatPKR(p.revenue)}</td></tr>
          `).join('') || '<tr><td colspan="3">No sales data yet</td></tr>'}
        </tbody>
      </table>`;
  }

  async function loadProducts() {
    document.getElementById('admin-title').textContent = 'Product Management';
    const [products, categories, sellers] = await Promise.all([
      MSA.request('/api/products?limit=100'),
      MSA.request('/api/categories'),
      MSA.request('/api/sellers'),
    ]);

    const catSelect = categories.map((c) => `<option value="${c.id}">${c.name}</option>`).join('');
    const sellerSelect = sellers.map((s) => `<option value="${s.id}">${s.business_name}</option>`).join('');

    document.getElementById('product-form-cats').innerHTML = catSelect;
    document.getElementById('product-form-sellers').innerHTML = sellerSelect;

    const tbody = document.querySelector('#products-table tbody');
    tbody.innerHTML = products.map((p) => `
      <tr>
        <td>${p.name}</td>
        <td>${p.category?.name || ''}</td>
        <td>${p.seller?.business_name || ''}</td>
        <td>${MSA.formatPKR(p.price)}</td>
        <td>${p.stock}</td>
        <td>${p.badge}</td>
        <td>
          <button class="btn btn-ghost" data-edit="${p.id}">Edit stock</button>
          <button class="btn btn-ghost" data-del="${p.id}">Deactivate</button>
        </td>
      </tr>`).join('');

    document.getElementById('product-create-form')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const f = e.target;
      const msg = document.getElementById('product-msg');
      try {
        await MSA.request('/api/products', {
          method: 'POST',
          body: JSON.stringify({
            name: f.name.value.trim(),
            description: f.description.value.trim(),
            features: f.features.value.trim() || null,
            price: Number(f.price.value),
            original_price: f.original_price.value ? Number(f.original_price.value) : null,
            stock: Number(f.stock.value || 0),
            badge: f.badge.value,
            warehouse_available: f.warehouse_available.checked,
            category_id: Number(f.category_id.value),
            seller_id: Number(f.seller_id.value),
            image_url: f.image_url.value.trim() || null,
          }),
        });
        msg.innerHTML = '<div class="alert alert-success">Product created</div>';
        MSA.toast('Product created');
        setTimeout(() => location.reload(), 700);
      } catch (err) {
        msg.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
      }
    });

    tbody.querySelectorAll('[data-del]').forEach((btn) => {
      btn.onclick = async () => {
        if (!confirm('Deactivate this product?')) return;
        await MSA.request(`/api/products/${btn.dataset.del}`, { method: 'DELETE' });
        MSA.toast('Product deactivated');
        location.reload();
      };
    });

    tbody.querySelectorAll('[data-edit]').forEach((btn) => {
      btn.onclick = async () => {
        const stock = prompt('New stock quantity');
        if (stock == null) return;
        await MSA.request(`/api/inventory/${btn.dataset.edit}`, {
          method: 'PUT',
          body: JSON.stringify({ quantity: Number(stock) }),
        });
        MSA.toast('Stock updated');
        location.reload();
      };
    });
  }

  async function loadOrders() {
    document.getElementById('admin-title').textContent = 'Order Management';
    const status = document.getElementById('order-status-filter')?.value || '';
    const qs = status ? `?status=${encodeURIComponent(status)}` : '';
    const orders = await MSA.request(`/api/orders${qs}`);
    const statuses = ['Order Placed', 'Confirmed', 'Packed', 'Shipped', 'Delivered', 'Cancelled', 'Returned'];
    const tbody = document.querySelector('#orders-table tbody');
    tbody.innerHTML = orders.map((o) => `
      <tr>
        <td>${o.order_number}</td>
        <td>${o.customer_name}<div style="font-size:0.75rem;opacity:0.6">${o.phone}</div></td>
        <td>${MSA.formatPKR(o.total_amount)}</td>
        <td>${o.city}</td>
        <td>
          <select data-status="${o.id}">
            ${statuses.map((s) => `<option value="${s}" ${s === o.status ? 'selected' : ''}>${s}</option>`).join('')}
          </select>
        </td>
        <td>${new Date(o.created_at).toLocaleString()}</td>
      </tr>`).join('') || '<tr><td colspan="6">No orders</td></tr>';

    tbody.querySelectorAll('[data-status]').forEach((sel) => {
      sel.onchange = async () => {
        try {
          await MSA.request(`/api/orders/${sel.dataset.status}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status: sel.value }),
          });
          MSA.toast('Order status updated');
        } catch (e) {
          MSA.toast(e.message, 'error');
        }
      };
    });

    document.getElementById('order-status-filter')?.addEventListener('change', loadOrders);
  }

  async function loadInventory() {
    document.getElementById('admin-title').textContent = 'Inventory Management';
    const [all, low, oos, wh] = await Promise.all([
      MSA.request('/api/inventory'),
      MSA.request('/api/inventory/low-stock'),
      MSA.request('/api/inventory/out-of-stock'),
      MSA.request('/api/inventory/warehouse'),
    ]);
    document.getElementById('inv-stats').innerHTML = `
      <div class="stat-card"><div class="label">Tracked SKUs</div><div class="value">${all.length}</div></div>
      <div class="stat-card amber"><div class="label">Low Stock</div><div class="value">${low.length}</div></div>
      <div class="stat-card amber"><div class="label">Out of Stock</div><div class="value">${oos.length}</div></div>
      <div class="stat-card gold"><div class="label">Warehouse</div><div class="value">${wh.length}</div></div>`;

    document.querySelector('#inventory-table tbody').innerHTML = all.map((i) => `
      <tr>
        <td>${i.product?.name || i.product_id}</td>
        <td>${i.quantity}</td>
        <td>${i.product?.stock_status || ''}</td>
        <td>${i.warehouse_location || '—'}</td>
        <td><button class="btn btn-ghost" data-inv="${i.product_id}">Update</button></td>
      </tr>`).join('');

    document.querySelectorAll('[data-inv]').forEach((btn) => {
      btn.onclick = async () => {
        const qty = prompt('Set quantity');
        if (qty == null) return;
        await MSA.request(`/api/inventory/${btn.dataset.inv}`, {
          method: 'PUT',
          body: JSON.stringify({ quantity: Number(qty) }),
        });
        MSA.toast('Inventory updated');
        loadInventory();
      };
    });
  }

  async function loadSellers() {
    document.getElementById('admin-title').textContent = 'Seller Management';
    const sellers = await MSA.request('/api/sellers');
    document.querySelector('#sellers-table tbody').innerHTML = sellers.map((s) => `
      <tr>
        <td>${s.business_name}</td>
        <td>${s.owner_name}</td>
        <td>${s.city}, ${s.district}</td>
        <td>${s.selling_type}</td>
        <td>${s.status}${s.is_verified ? ' · Verified' : ''}</td>
        <td>
          <button class="btn btn-teal" data-approve="${s.id}">Approve</button>
          <button class="btn btn-ghost" data-reject="${s.id}">Reject</button>
        </td>
      </tr>`).join('');

    document.querySelectorAll('[data-approve]').forEach((btn) => {
      btn.onclick = async () => {
        await MSA.request(`/api/sellers/${btn.dataset.approve}/status`, {
          method: 'PUT',
          body: JSON.stringify({ status: 'approved', is_verified: true }),
        });
        MSA.toast('Seller approved');
        loadSellers();
      };
    });
    document.querySelectorAll('[data-reject]').forEach((btn) => {
      btn.onclick = async () => {
        await MSA.request(`/api/sellers/${btn.dataset.reject}/status`, {
          method: 'PUT',
          body: JSON.stringify({ status: 'rejected', is_verified: false }),
        });
        MSA.toast('Seller rejected');
        loadSellers();
      };
    });
  }

  async function loadReports() {
    document.getElementById('admin-title').textContent = 'Reports & Analytics';
    const [sales, top, inv, delivery, customers] = await Promise.all([
      MSA.request('/api/reports/sales'),
      MSA.request('/api/reports/top-products'),
      MSA.request('/api/reports/inventory'),
      MSA.request('/api/reports/delivery'),
      MSA.request('/api/reports/customers'),
    ]);
    document.getElementById('report-cards').innerHTML = `
      <div class="stat-card"><div class="label">Daily Sales</div><div class="value">${MSA.formatPKR(sales.daily_sales)}</div></div>
      <div class="stat-card gold"><div class="label">Monthly Sales</div><div class="value">${MSA.formatPKR(sales.monthly_sales)}</div></div>
      <div class="stat-card"><div class="label">Total Orders</div><div class="value">${sales.total_orders}</div></div>
      <div class="stat-card"><div class="label">Revenue</div><div class="value">${MSA.formatPKR(sales.revenue)}</div></div>
      <div class="stat-card"><div class="label">In Stock</div><div class="value">${inv.in_stock}</div><div class="sub">Low ${inv.low_stock} · OOS ${inv.out_of_stock}</div></div>
      <div class="stat-card gold"><div class="label">Delivery On-time</div><div class="value">${delivery.on_time_rate}%</div><div class="sub">${delivery.note}</div></div>
      <div class="stat-card"><div class="label">Customers</div><div class="value">${customers.total_customers}</div><div class="sub">+${customers.new_this_week} this week</div></div>
      <div class="stat-card amber"><div class="label">Warehouse SKUs</div><div class="value">${inv.warehouse}</div></div>`;

    document.getElementById('report-top').innerHTML = `
      <div class="panel-head"><h2>Top Selling Products</h2></div>
      <table>
        <thead><tr><th>Product</th><th>Sold</th><th>Revenue</th></tr></thead>
        <tbody>
          ${top.map((p) => `<tr><td>${p.name}</td><td>${p.sold}</td><td>${MSA.formatPKR(p.revenue)}</td></tr>`).join('') || '<tr><td colspan="3">No data</td></tr>'}
        </tbody>
      </table>`;
  }
})();
