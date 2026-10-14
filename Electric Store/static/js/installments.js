let installments = [];
const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));

function statusBadge(status) {
  const map = {
    active: 'bg-primary',
    overdue: 'bg-danger',
    completed: 'bg-success',
  };
  return `<span class="badge ${map[status] || 'bg-secondary'}">${status}</span>`;
}

async function loadInstallments() {
  installments = await apiFetch('/api/installments/');
  const tbody = document.querySelector('#installmentsTable tbody');
  tbody.innerHTML = installments.map(i => `
    <tr>
      <td><strong>${i.customer_name}</strong></td>
      <td>${i.product_name}</td>
      <td>${formatCurrency(i.total_amount)}</td>
      <td>${formatCurrency(i.down_payment)}</td>
      <td class="fw-bold text-warning">${formatCurrency(i.remaining_balance)}</td>
      <td>${formatCurrency(i.monthly_amount)}</td>
      <td>${i.next_due_date || '—'}</td>
      <td>${statusBadge(i.status)}</td>
      <td>
        ${i.status !== 'completed'
          ? `<button class="btn btn-sm btn-success" onclick="openPayment(${i.id})"><i class="bi bi-cash"></i> Pay</button>`
          : '—'}
      </td>
    </tr>
  `).join('');
}

window.openPayment = function(id) {
  const inst = installments.find(x => x.id === id);
  if (!inst) return;
  document.getElementById('paymentInstallmentId').value = id;
  document.getElementById('paymentInfo').textContent =
    `${inst.customer_name} — ${inst.product_name} | Remaining: ${formatCurrency(inst.remaining_balance)}`;
  document.getElementById('paymentAmount').value = inst.monthly_amount;
  document.getElementById('paymentAmount').max = inst.remaining_balance;
  paymentModal.show();
};

document.getElementById('paymentForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const id = document.getElementById('paymentInstallmentId').value;
  try {
    const result = await apiFetch(`/api/installments/${id}/pay`, {
      method: 'POST',
      body: {
        amount: parseFloat(document.getElementById('paymentAmount').value),
        notes: document.getElementById('paymentNotes').value,
      },
    });
    alert(`Payment recorded! Remaining: ${formatCurrency(result.remaining_balance)}`);
    paymentModal.hide();
    loadInstallments();
  } catch (err) {
    alert(err.message);
  }
});

loadInstallments();
