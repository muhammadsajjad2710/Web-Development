let productList = [];

function updateSaleCalc() {
  const productId = document.getElementById('saleProduct').value;
  const qty = parseInt(document.getElementById('saleQty').value) || 1;
  const product = productList.find(p => p.id == productId);
  const unitPrice = product ? product.sale_price : 0;
  const total = unitPrice * qty;

  document.getElementById('saleUnitPrice').value = formatCurrency(unitPrice);
  document.getElementById('saleTotal').textContent = formatCurrency(total);

  const type = document.getElementById('saleType').value;
  if (type === 'installment') {
    const down = parseFloat(document.getElementById('saleDown').value) || 0;
    const months = parseInt(document.getElementById('saleMonths').value) || 1;
    const remaining = Math.max(total - down, 0);
    document.getElementById('saleMonthly').value = formatCurrency(remaining / months);
  }
}

async function loadSales() {
  const sales = await apiFetch('/api/sales/');
  const tbody = document.querySelector('#salesTable tbody');
  tbody.innerHTML = sales.map(s => `
    <tr>
      <td><strong>${s.invoice_no}</strong></td>
      <td>${new Date(s.sale_date).toLocaleDateString()}</td>
      <td>${s.product_name}</td>
      <td>${s.customer_name}</td>
      <td><span class="badge ${s.sale_type === 'cash' ? 'bg-success' : 'bg-warning text-dark'}">${s.sale_type}</span></td>
      <td>${formatCurrency(s.total_amount)}</td>
      <td>${s.remaining_amount > 0 ? formatCurrency(s.remaining_amount) : '—'}</td>
    </tr>
  `).join('');
}

async function loadFormData() {
  productList = await apiFetch('/api/products/');
  const customers = await apiFetch('/api/customers/');

  document.getElementById('saleProduct').innerHTML = productList.map(p =>
    `<option value="${p.id}">${p.name} (Stock: ${p.quantity}) — ${formatCurrency(p.sale_price)}</option>`
  ).join('');

  document.getElementById('saleCustomer').innerHTML =
    '<option value="">Walk-in Customer</option>' +
    customers.map(c => `<option value="${c.id}">${c.name} — ${c.phone}</option>`).join('');

  updateSaleCalc();
}

document.getElementById('saleType').addEventListener('change', () => {
  const isInst = document.getElementById('saleType').value === 'installment';
  document.getElementById('installmentFields').classList.toggle('d-none', !isInst);
  updateSaleCalc();
});

['saleProduct', 'saleQty', 'saleDown', 'saleMonths'].forEach(id => {
  document.getElementById(id).addEventListener('input', updateSaleCalc);
});

document.getElementById('saleForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const type = document.getElementById('saleType').value;
  const customerId = document.getElementById('saleCustomer').value;

  const body = {
    product_id: parseInt(document.getElementById('saleProduct').value),
    customer_id: customerId ? parseInt(customerId) : null,
    sale_type: type,
    quantity: parseInt(document.getElementById('saleQty').value),
    down_payment: type === 'installment' ? parseFloat(document.getElementById('saleDown').value) : 0,
    total_months: type === 'installment' ? parseInt(document.getElementById('saleMonths').value) : 12,
  };

  try {
    const sale = await apiFetch('/api/sales/', { method: 'POST', body });
    alert(`Sale created! Invoice: ${sale.invoice_no}`);
    bootstrap.Modal.getInstance(document.getElementById('saleModal')).hide();
    loadSales();
    loadFormData();
  } catch (err) {
    alert(err.message);
  }
});

loadSales();
loadFormData();
