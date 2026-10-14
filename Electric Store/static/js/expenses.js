const expenseModal = new bootstrap.Modal(document.getElementById('expenseModal'));

document.getElementById('expenseDate').value = new Date().toISOString().split('T')[0];

async function loadExpenses() {
  const expenses = await apiFetch('/api/expenses/');
  const tbody = document.querySelector('#expensesTable tbody');
  tbody.innerHTML = expenses.map(e => `
    <tr>
      <td>${e.expense_date}</td>
      <td><span class="badge bg-secondary">${e.category}</span></td>
      <td>${e.description || '—'}</td>
      <td class="fw-bold text-danger">${formatCurrency(e.amount)}</td>
    </tr>
  `).join('');
}

document.getElementById('expenseForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  await apiFetch('/api/expenses/', {
    method: 'POST',
    body: {
      category: document.getElementById('expenseCategory').value,
      description: document.getElementById('expenseDesc').value,
      amount: parseFloat(document.getElementById('expenseAmount').value),
      expense_date: document.getElementById('expenseDate').value,
    },
  });
  expenseModal.hide();
  document.getElementById('expenseForm').reset();
  document.getElementById('expenseDate').value = new Date().toISOString().split('T')[0];
  loadExpenses();
});

loadExpenses();
