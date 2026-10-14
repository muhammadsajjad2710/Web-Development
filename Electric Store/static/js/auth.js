if (!getToken() && !window.location.pathname.endsWith('/') && window.location.pathname !== '') {
  window.location.href = '/';
}

const adminName = localStorage.getItem('full_name');
if (adminName) {
  const el = document.getElementById('adminName');
  if (el) el.textContent = adminName;
}

document.getElementById('logoutBtn')?.addEventListener('click', () => {
  localStorage.removeItem('token');
  localStorage.removeItem('full_name');
  window.location.href = '/';
});

document.getElementById('sidebarToggle')?.addEventListener('click', () => {
  document.getElementById('sidebar')?.classList.toggle('show');
});
