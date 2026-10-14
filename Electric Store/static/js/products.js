let products = [];
const modal = new bootstrap.Modal(document.getElementById('productModal'));

function productImageCell(p) {
  if (p.image_path) {
    return `<img src="${p.image_path}" class="product-thumb" alt="${p.name}">`;
  }
  return `<div class="product-placeholder"><i class="bi bi-image"></i></div>`;
}

function stockBadge(qty, threshold) {
  if (qty <= threshold) return `<span class="badge bg-danger">Low (${qty})</span>`;
  return `<span class="badge bg-success">${qty}</span>`;
}

async function loadProducts() {
  products = await apiFetch('/api/products/');
  const tbody = document.querySelector('#productsTable tbody');
  tbody.innerHTML = products.map(p => `
    <tr>
      <td>${productImageCell(p)}</td>
      <td><strong>${p.name}</strong><br><small class="text-muted">${p.description || ''}</small></td>
      <td>${p.quantity}</td>
      <td>${formatCurrency(p.purchase_price)}</td>
      <td>${formatCurrency(p.sale_price)}</td>
      <td>${stockBadge(p.quantity, p.low_stock_threshold)}</td>
      <td>
        <button class="btn btn-sm btn-outline-primary me-1" onclick="editProduct(${p.id})"><i class="bi bi-pencil"></i></button>
        <button class="btn btn-sm btn-outline-danger" onclick="deleteProduct(${p.id})"><i class="bi bi-trash"></i></button>
      </td>
    </tr>
  `).join('');
}

window.editProduct = function(id) {
  const p = products.find(x => x.id === id);
  if (!p) return;
  document.getElementById('productModalTitle').textContent = 'Edit Product';
  document.getElementById('productId').value = p.id;
  document.getElementById('productName').value = p.name;
  document.getElementById('productDesc').value = p.description || '';
  document.getElementById('productQty').value = p.quantity;
  document.getElementById('productPurchase').value = p.purchase_price;
  document.getElementById('productSale').value = p.sale_price;
  document.getElementById('productThreshold').value = p.low_stock_threshold;
  modal.show();
};

window.deleteProduct = async function(id) {
  if (!confirm('Delete this product?')) return;
  await apiFetch(`/api/products/${id}`, { method: 'DELETE' });
  loadProducts();
};

document.getElementById('addProductBtn').addEventListener('click', () => {
  document.getElementById('productModalTitle').textContent = 'Add Product';
  document.getElementById('productForm').reset();
  document.getElementById('productId').value = '';
});

document.getElementById('productForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('productId').value;
  const formData = new FormData();
  formData.append('name', document.getElementById('productName').value);
  formData.append('description', document.getElementById('productDesc').value);
  formData.append('quantity', document.getElementById('productQty').value);
  formData.append('purchase_price', document.getElementById('productPurchase').value);
  formData.append('sale_price', document.getElementById('productSale').value);
  formData.append('low_stock_threshold', document.getElementById('productThreshold').value);
  const image = document.getElementById('productImage').files[0];
  if (image) formData.append('image', image);

  const url = id ? `/api/products/${id}` : '/api/products/';
  await apiFetch(url, { method: id ? 'PUT' : 'POST', body: formData });
  modal.hide();
  loadProducts();
});

loadProducts();
