const customerModal = new bootstrap.Modal(document.getElementById('customerModal'));

async function loadCustomers() {
  const customers = await apiFetch('/api/customers/');
  const tbody = document.querySelector('#customersTable tbody');
  tbody.innerHTML = customers.map(c => `
    <tr>
      <td><strong>${c.name}</strong></td>
      <td>${c.phone}</td>
      <td>${c.cnic || '—'}</td>
      <td>${c.address || '—'}</td>
      <td>
        <button class="btn btn-sm btn-outline-danger" onclick="deleteCustomer(${c.id})"><i class="bi bi-trash"></i></button>
      </td>
    </tr>
  `).join('');
}

window.deleteCustomer = async function(id) {
  if (!confirm('Delete this customer?')) return;
  try {
    await apiFetch(`/api/customers/${id}`, { method: 'DELETE' });
    loadCustomers();
  } catch (err) {
    alert(err.message);
  }
};

document.getElementById('customerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  await apiFetch('/api/customers/', {
    method: 'POST',
    body: {
      name: document.getElementById('customerName').value,
      phone: document.getElementById('customerPhone').value,
      cnic: document.getElementById('customerCnic').value,
      address: document.getElementById('customerAddress').value,
    },
  });
  customerModal.hide();
  document.getElementById('customerForm').reset();
  loadCustomers();
});

loadCustomers();
