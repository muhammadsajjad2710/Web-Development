/**
 * Dashboard shell: sidebar, topbar, auth gate
 */
(function (global) {
  const NAV = [
    { href: "index.html", label: "Dashboard", icon: "◆" },
    { href: "orders.html", label: "Orders", icon: "☰" },
    { href: "menu.html", label: "Menu", icon: "▦" },
    { href: "branches.html", label: "Branches", icon: "⌖" },
    { href: "customers.html", label: "Customers", icon: "☺" },
    { href: "crm.html", label: "CRM", icon: "✎" },
    { href: "whatsapp.html", label: "WhatsApp", icon: "◉" },
    { href: "reports.html", label: "Reports", icon: "▤" },
    { href: "staff.html", label: "Staff", icon: "☷" },
    { href: "subscription.html", label: "Subscription", icon: "★" },
    { href: "settings.html", label: "Settings", icon: "⚙" },
  ];

  function currentPage() {
    const parts = window.location.pathname.split("/");
    return parts[parts.length - 1] || "index.html";
  }

  function renderShell(options = {}) {
    if (!ORApi.requireAuth("../auth/login.html")) return null;
    const user = ORApi.getUser();
    const page = currentPage();
    const title = options.title || "Dashboard";

    const navHtml = NAV.map(
      (item) => `
      <a class="nav-item ${item.href === page ? "active" : ""}" href="${item.href}">
        <span class="nav-icon">${item.icon}</span>
        ${item.label}
      </a>`
    ).join("");

    const root = document.getElementById("app");
    root.innerHTML = `
      <div class="sidebar-backdrop" id="sidebar-backdrop"></div>
      <div class="app-shell">
        <aside class="sidebar" id="sidebar">
          <div class="sidebar-brand">
            <span class="brand-mark" style="width:32px;height:32px;border-radius:8px;background:linear-gradient(145deg,#2f6bb3,#4f8bc9);display:grid;place-items:center;font-size:.75rem;">OR</span>
            <span>Online Restaurant</span>
          </div>
          <nav class="sidebar-nav">${navHtml}</nav>
          <div class="sidebar-footer">MSA Technologies · v1.0</div>
        </aside>
        <div class="main-area">
          <header class="topbar">
            <div class="flex gap-1" style="align-items:center;">
              <button class="mobile-toggle" id="menu-toggle" type="button" aria-label="Menu">☰</button>
              <div class="topbar-title">${title}</div>
            </div>
            <div class="topbar-actions">
              <a class="btn btn-outline btn-sm hide-mobile" href="../restaurant/index.html?slug=lahore-spice-house" target="_blank">Public site</a>
              <div class="user-chip">
                <div class="avatar">${ORUI.initials(user?.full_name)}</div>
                <div class="user-meta">
                  <strong>${user?.full_name || "User"}</strong>
                  <span>${user?.role?.display_name || user?.role?.name || ""}</span>
                </div>
              </div>
              <button class="btn btn-ghost btn-sm" id="logout-btn" type="button">Logout</button>
            </div>
          </header>
          <main class="content" id="page-content">
            <div class="spinner"></div>
          </main>
        </div>
      </div>
    `;

    document.getElementById("logout-btn").addEventListener("click", () => {
      ORApi.clearSession();
      window.location.href = "../auth/login.html";
    });

    const sidebar = document.getElementById("sidebar");
    const backdrop = document.getElementById("sidebar-backdrop");
    document.getElementById("menu-toggle").addEventListener("click", () => {
      sidebar.classList.toggle("open");
      backdrop.classList.toggle("show");
    });
    backdrop.addEventListener("click", () => {
      sidebar.classList.remove("open");
      backdrop.classList.remove("show");
    });

    return document.getElementById("page-content");
  }

  function renderSalesChart(container, salesByDay) {
    if (!container) return;
    const max = Math.max(...salesByDay.map((d) => d.revenue), 1);
    container.innerHTML = `
      <div class="chart-bars">
        ${salesByDay
          .map((d) => {
            const h = Math.max(8, Math.round((d.revenue / max) * 160));
            const label = d.date.slice(5);
            return `<div class="chart-bar" style="height:${h}px" title="${ORUI.formatPKR(d.revenue)}"><span>${label}</span></div>`;
          })
          .join("")}
      </div>
    `;
  }

  global.ORDashboard = { renderShell, renderSalesChart, NAV };
})(window);
