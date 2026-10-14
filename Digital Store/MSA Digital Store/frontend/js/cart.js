document.addEventListener('DOMContentLoaded', async () => {
  const root = document.getElementById('cart-root');
  if (!root) return;

  async function render() {
    const auth = MSA.getToken();
    let items = [];
    let subtotal = 0;
    let delivery = 150;
    let total = 0;

    if (auth?.role === 'customer' && auth.access_token) {
      try {
        const cart = await MSA.request('/api/cart/me');
        items = (cart.items || []).map((i) => ({
          id: i.id,
          product_id: i.product_id,
          quantity: i.quantity,
          name: i.product?.name,
          price: i.product?.price,
          image: MSA.productImage(i.product || {}),
          seller: i.product?.seller?.business_name,
          stock: i.product?.stock,
          server: true,
        }));
        subtotal = cart.subtotal;
        delivery = cart.delivery_charges;
        total = cart.total;
      } catch (e) {
        root.innerHTML = `<div class="alert alert-error">${e.message}</div>`;
        return;
      }
    } else {
      items = MSA.getGuestCart().map((i) => ({ ...i, server: false }));
      subtotal = items.reduce((s, i) => s + i.price * i.quantity, 0);
      delivery = subtotal === 0 || subtotal >= 5000 ? 0 : 150;
      total = subtotal + delivery;
    }

    if (!items.length) {
      root.innerHTML = `
        <div class="panel" style="text-align:center;padding:3rem">
          <h2 class="font-display">Your cart is empty</h2>
          <p class="muted">Browse the marketplace and add products to get started.</p>
          <a class="btn btn-teal" href="products.html" style="margin-top:1rem">Start Shopping</a>
        </div>`;
      return;
    }

    root.innerHTML = `
      <div class="cart-layout">
        <div id="cart-items">
          ${items.map((item, idx) => `
            <div class="cart-item" data-idx="${idx}">
              <img src="${item.image}" alt="${item.name}" />
              <div style="flex:1">
                <div style="display:flex;justify-content:space-between;gap:1rem">
                  <div>
                    <a href="product-detail.html?id=${item.product_id}"><strong>${item.name}</strong></a>
                    <div class="muted" style="font-size:0.78rem">Sold by ${item.seller || 'Seller'}</div>
                  </div>
                  <button type="button" class="btn btn-outline-dark" data-remove="${idx}" style="padding:0.4rem 0.7rem">Remove</button>
                </div>
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.75rem;flex-wrap:wrap;gap:0.75rem">
                  <div class="qty-box">
                    <button type="button" data-dec="${idx}">−</button>
                    <span>${item.quantity}</span>
                    <button type="button" data-inc="${idx}">+</button>
                  </div>
                  <strong>${MSA.formatPKR(item.price * item.quantity)}</strong>
                </div>
              </div>
            </div>`).join('')}
        </div>
        <aside class="summary-card">
          <h3 class="font-display" style="margin-top:0">Order Summary</h3>
          <div class="summary-row"><span>Subtotal</span><span>${MSA.formatPKR(subtotal)}</span></div>
          <div class="summary-row"><span>Delivery charges</span><span>${delivery === 0 ? 'Free' : MSA.formatPKR(delivery)}</span></div>
          ${delivery > 0 ? `<p class="muted" style="font-size:0.78rem;background:rgba(20,184,166,0.1);padding:0.6rem;border-radius:8px">Add ${MSA.formatPKR(5000 - subtotal)} more for free delivery</p>` : ''}
          <div class="summary-total"><span>Total</span><span>${MSA.formatPKR(total)}</span></div>
          <a class="btn btn-teal" href="checkout.html" style="width:100%;margin-top:1rem">Proceed to Checkout</a>
          <a class="muted" href="products.html" style="display:block;text-align:center;margin-top:0.75rem;font-size:0.85rem">Continue shopping</a>
        </aside>
      </div>`;

    root.querySelectorAll('[data-remove]').forEach((btn) => {
      btn.onclick = async () => {
        const idx = Number(btn.dataset.remove);
        const item = items[idx];
        if (item.server) {
          await MSA.request(`/api/cart/item/${item.id}`, { method: 'DELETE' });
        } else {
          const cart = MSA.getGuestCart();
          cart.splice(idx, 1);
          MSA.setGuestCart(cart);
        }
        MSA.toast('Item removed');
        render();
        MSA.updateCartBadge();
      };
    });

    root.querySelectorAll('[data-inc], [data-dec]').forEach((btn) => {
      btn.onclick = async () => {
        const idx = Number(btn.dataset.inc ?? btn.dataset.dec);
        const item = items[idx];
        const nextQty = btn.dataset.inc != null ? item.quantity + 1 : Math.max(1, item.quantity - 1);
        if (item.server) {
          await MSA.request(`/api/cart/item/${item.id}`, {
            method: 'PUT',
            body: JSON.stringify({ quantity: nextQty }),
          });
        } else {
          const cart = MSA.getGuestCart();
          cart[idx].quantity = nextQty;
          MSA.setGuestCart(cart);
        }
        render();
        MSA.updateCartBadge();
      };
    });
  }

  render();
});
