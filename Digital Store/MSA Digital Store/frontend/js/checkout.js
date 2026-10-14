document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('checkout-form');
  if (!form) return;

  const summary = document.getElementById('checkout-summary');
  const auth = MSA.getToken();

  async function loadSummary() {
    let items = [];
    let subtotal = 0;
    let delivery = 150;
    let total = 0;

    if (auth?.role === 'customer' && auth.access_token) {
      try {
        const cart = await MSA.request('/api/cart/me');
        items = cart.items || [];
        subtotal = cart.subtotal;
        delivery = cart.delivery_charges;
        total = cart.total;
        if (auth.full_name) form.customer_name.value = auth.full_name;
      } catch { /* guest fallback below */ }
    }

    if (!items.length) {
      const guest = MSA.getGuestCart();
      items = guest.map((g) => ({ quantity: g.quantity, product: { name: g.name, price: g.price }, product_id: g.product_id }));
      subtotal = guest.reduce((s, i) => s + i.price * i.quantity, 0);
      delivery = subtotal === 0 || subtotal >= 5000 ? 0 : 150;
      total = subtotal + delivery;
    }

    if (!items.length) {
      summary.innerHTML = `<p class="muted">Your cart is empty.</p><a class="btn btn-teal" href="products.html">Browse Products</a>`;
      form.querySelector('button[type="submit"]').disabled = true;
      return { empty: true };
    }

    summary.innerHTML = `
      <h3 class="font-display" style="margin-top:0">Order Summary</h3>
      <ul style="list-style:none;padding:0;margin:0 0 1rem;max-height:220px;overflow:auto">
        ${items.map((i) => {
          const name = i.product?.name || i.name;
          const price = i.product?.price ?? i.price;
          return `<li class="summary-row"><span>${name} × ${i.quantity}</span><span>${MSA.formatPKR(price * i.quantity)}</span></li>`;
        }).join('')}
      </ul>
      <div class="summary-row"><span>Subtotal</span><span>${MSA.formatPKR(subtotal)}</span></div>
      <div class="summary-row"><span>Delivery</span><span>${delivery === 0 ? 'Free' : MSA.formatPKR(delivery)}</span></div>
      <div class="summary-total"><span>Total</span><span>${MSA.formatPKR(total)}</span></div>
      <p class="muted" style="font-size:0.72rem;margin-top:0.75rem;text-align:center">Payment gateway & courier integrations coming soon</p>`;
    return { empty: false, guestItems: MSA.getGuestCart() };
  }

  form.querySelectorAll('input[name="payment_method"]').forEach((radio) => {
    radio.addEventListener('change', () => {
      form.querySelectorAll('.pay-option').forEach((el) => el.classList.remove('selected'));
      radio.closest('.pay-option')?.classList.add('selected');
    });
  });

  loadSummary().then((state) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const msg = document.getElementById('checkout-msg');
      msg.innerHTML = '';
      const payload = {
        customer_name: form.customer_name.value.trim(),
        phone: form.phone.value.trim(),
        email: form.email.value.trim() || null,
        address: form.address.value.trim(),
        city: form.city.value.trim(),
        district: form.district.value.trim(),
        payment_method: form.payment_method.value,
        notes: form.notes.value.trim() || null,
      };

      const useGuest = !(auth?.role === 'customer' && auth.access_token) || (state.guestItems?.length && !(await hasServerCart()));
      if (useGuest) {
        const guest = MSA.getGuestCart();
        if (!guest.length) {
          msg.innerHTML = '<div class="alert alert-error">Cart is empty</div>';
          return;
        }
        payload.guest_items = guest.map((g) => ({ product_id: g.product_id, quantity: g.quantity }));
      }

      const btn = form.querySelector('button[type="submit"]');
      btn.disabled = true;
      btn.textContent = 'Placing order…';
      try {
        const order = await MSA.request('/api/orders', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
        MSA.setGuestCart([]);
        MSA.updateCartBadge();
        MSA.toast('Order placed successfully');
        document.getElementById('checkout-root').innerHTML = `
          <div class="panel" style="text-align:center;max-width:520px;margin:0 auto;padding:2.5rem">
            <h2 class="font-display">Order Placed Successfully</h2>
            <p class="muted">Thank you for shopping with MSA Digital Store.</p>
            <p style="margin:1rem 0"><strong>Order ID: ${order.order_number}</strong></p>
            <a class="btn btn-navy" href="order-tracking.html?order=${order.order_number}">Track Your Order</a>
          </div>`;
      } catch (err) {
        msg.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
        btn.disabled = false;
        btn.textContent = 'Place Order';
      }
    });
  });

  async function hasServerCart() {
    try {
      const cart = await MSA.request('/api/cart/me');
      return (cart.items || []).length > 0;
    } catch {
      return false;
    }
  }

  // Login / Register page
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  document.querySelectorAll('[data-auth-tab]').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('[data-auth-tab]').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const tab = btn.dataset.authTab;
      if (loginForm) loginForm.style.display = tab === 'login' ? 'grid' : 'none';
      if (registerForm) registerForm.style.display = tab === 'register' ? 'grid' : 'none';
    });
  });

  loginForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = document.getElementById('auth-msg');
    try {
      const data = await MSA.request('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({
          email: loginForm.email.value.trim(),
          password: loginForm.password.value,
        }),
      });
      MSA.setAuth(data);
      MSA.toast('Logged in successfully');
      if (data.role === 'admin') location.href = 'admin/dashboard.html';
      else location.href = 'index.html';
    } catch (err) {
      msg.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
    }
  });

  registerForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = document.getElementById('auth-msg');
    try {
      const data = await MSA.request('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({
          full_name: registerForm.full_name.value.trim(),
          email: registerForm.email.value.trim(),
          phone: registerForm.phone.value.trim() || null,
          password: registerForm.password.value,
          city: registerForm.city.value.trim() || null,
          district: registerForm.district.value.trim() || null,
        }),
      });
      MSA.setAuth(data);
      MSA.toast('Account created');
      location.href = 'index.html';
    } catch (err) {
      msg.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
    }
  });

  // Seller registration
  const sellerForm = document.getElementById('seller-form');
  sellerForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = document.getElementById('seller-msg');
    const btn = sellerForm.querySelector('button[type="submit"]');
    btn.disabled = true;
    try {
      await MSA.request('/api/sellers/register', {
        method: 'POST',
        body: JSON.stringify({
          business_name: sellerForm.business_name.value.trim(),
          owner_name: sellerForm.owner_name.value.trim(),
          phone: sellerForm.phone.value.trim(),
          email: sellerForm.email.value.trim(),
          business_category: sellerForm.business_category.value,
          business_address: sellerForm.business_address.value.trim(),
          city: sellerForm.city.value.trim(),
          district: sellerForm.district.value.trim(),
          cnic: sellerForm.cnic.value.trim() || null,
          ntn: sellerForm.ntn.value.trim() || null,
          selling_type: sellerForm.selling_type.value,
          password: sellerForm.password.value || null,
        }),
      });
      msg.innerHTML = '<div class="alert alert-success">Application submitted. Our team will contact you shortly.</div>';
      sellerForm.reset();
      MSA.toast('Seller application submitted');
    } catch (err) {
      msg.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
    } finally {
      btn.disabled = false;
    }
  });

  // Order tracking
  const trackForm = document.getElementById('track-form');
  const trackResult = document.getElementById('track-result');
  const prefill = new URLSearchParams(location.search).get('order');
  if (prefill && trackForm) {
    trackForm.order_number.value = prefill;
    trackOrder(prefill);
  }
  trackForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    trackOrder(trackForm.order_number.value.trim());
  });

  async function trackOrder(orderNumber) {
    if (!trackResult || !orderNumber) return;
    trackResult.innerHTML = '<p class="loading">Looking up order…</p>';
    try {
      const order = await MSA.request(`/api/orders/track/${encodeURIComponent(orderNumber)}`);
      const flow = ['Order Placed', 'Confirmed', 'Packed', 'Shipped', 'Delivered'];
      let current = flow.indexOf(order.status);
      if (order.status === 'Cancelled' || order.status === 'Returned') current = -1;
      trackResult.innerHTML = `
        <div class="panel" style="padding:0;overflow:hidden">
          <div style="background:var(--navy-900);color:white;padding:1.25rem 1.5rem">
            <div style="color:var(--teal-400);font-size:0.85rem">Order Tracking</div>
            <h2 class="font-display" style="margin:0.25rem 0 0.75rem">${order.order_number}</h2>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.75rem;font-size:0.85rem;color:rgba(255,255,255,0.7)">
              <div><div style="opacity:0.5;font-size:0.68rem;text-transform:uppercase">Customer</div>${order.customer_name}</div>
              <div><div style="opacity:0.5;font-size:0.68rem;text-transform:uppercase">Status</div>${order.status}</div>
              <div><div style="opacity:0.5;font-size:0.68rem;text-transform:uppercase">Total</div>${MSA.formatPKR(order.total_amount)}</div>
            </div>
          </div>
          <div style="padding:1.5rem">
            <p class="muted" style="font-size:0.88rem">Items: ${order.items.map((i) => i.product_name).join(', ')}<br/>Deliver to: ${order.address}, ${order.city}, ${order.district}</p>
            ${current < 0 ? `<div class="alert alert-error">Order ${order.status}</div>` : ''}
            <ol class="timeline">
              ${flow.map((label, i) => `
                <li class="${i <= current ? 'done' : ''} ${i === current ? 'current' : ''}">
                  <div class="tl-dot">${i + 1}</div>
                  <div>
                    <strong>${label}</strong>
                    ${i === current ? '<span class="pill pill-verified" style="margin-left:0.4rem">Current</span>' : ''}
                  </div>
                </li>`).join('')}
            </ol>
          </div>
        </div>`;
    } catch (err) {
      trackResult.innerHTML = `<div class="alert alert-error">${err.message}</div>`;
    }
  }
});
