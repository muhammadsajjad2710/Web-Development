async function loadDashboard() {
  const stats = await apiFetch('/api/dashboard/stats');
  document.getElementById('todaySales').textContent = formatCurrency(stats.today_sales);
  document.getElementById('totalProducts').textContent = stats.total_products;
  document.getElementById('installmentsDue').textContent = stats.installments_due;
  document.getElementById('monthlyProfit').textContent = formatCurrency(stats.monthly_profit);
  document.getElementById('remainingInstallments').textContent = formatCurrency(stats.remaining_installments);
  document.getElementById('monthlyExpenses').textContent = formatCurrency(stats.monthly_expenses);
  document.getElementById('lowStock').textContent = stats.low_stock_count + ' items';

  const charts = await apiFetch('/api/dashboard/charts');

  new Chart(document.getElementById('salesChart'), {
    type: 'bar',
    data: {
      labels: charts.sales_by_month.map(d => d.month),
      datasets: [{
        label: 'Sales (Rs.)',
        data: charts.sales_by_month.map(d => d.amount),
        backgroundColor: '#2563eb',
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });

  new Chart(document.getElementById('expenseChart'), {
    type: 'doughnut',
    data: {
      labels: charts.expense_data.map(d => d.category),
      datasets: [{
        data: charts.expense_data.map(d => d.amount),
        backgroundColor: ['#2563eb', '#16a34a', '#d97706', '#dc2626', '#7c3aed'],
      }],
    },
    options: { responsive: true },
  });

  new Chart(document.getElementById('stockChart'), {
    type: 'bar',
    data: {
      labels: charts.stock_data.map(d => d.name),
      datasets: [{
        label: 'Stock Qty',
        data: charts.stock_data.map(d => d.quantity),
        backgroundColor: '#16a34a',
        borderRadius: 6,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { x: { beginAtZero: true } },
    },
  });
}

loadDashboard().catch(console.error);
