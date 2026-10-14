/**
 * Public restaurant cart helpers
 */
(function (global) {
  const KEY = "or_cart";

  function getSlug() {
    return new URLSearchParams(location.search).get("slug") || "lahore-spice-house";
  }

  function cartKey() {
    return `${KEY}_${getSlug()}`;
  }

  function getCart() {
    try {
      return JSON.parse(localStorage.getItem(cartKey()) || '{"items":[]}');
    } catch {
      return { items: [] };
    }
  }

  function saveCart(cart) {
    localStorage.setItem(cartKey(), JSON.stringify(cart));
    global.dispatchEvent(new CustomEvent("or:cart-updated"));
  }

  function addItem(item, qty = 1) {
    const cart = getCart();
    const existing = cart.items.find((i) => i.menu_item_id === item.id);
    if (existing) existing.quantity += qty;
    else {
      cart.items.push({
        menu_item_id: item.id,
        name: item.name,
        unit_price: Number(item.discount_price || item.price),
        quantity: qty,
      });
    }
    saveCart(cart);
    return cart;
  }

  function updateQty(menuItemId, quantity) {
    const cart = getCart();
    cart.items = cart.items
      .map((i) => (i.menu_item_id === menuItemId ? { ...i, quantity } : i))
      .filter((i) => i.quantity > 0);
    saveCart(cart);
    return cart;
  }

  function clear() {
    saveCart({ items: [] });
  }

  function totals() {
    const cart = getCart();
    const subtotal = cart.items.reduce((s, i) => s + i.unit_price * i.quantity, 0);
    return { items: cart.items, subtotal, count: cart.items.reduce((n, i) => n + i.quantity, 0) };
  }

  global.ORCart = { getSlug, getCart, addItem, updateQty, clear, totals };
})(window);
