/**
 * Auth helpers and toast UI
 */
(function (global) {
  function toast(message, type = "info") {
    let stack = document.querySelector(".toast-stack");
    if (!stack) {
      stack = document.createElement("div");
      stack.className = "toast-stack";
      document.body.appendChild(stack);
    }
    const el = document.createElement("div");
    el.className = `toast ${type}`;
    el.textContent = message;
    stack.appendChild(el);
    setTimeout(() => {
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 250);
    }, 3200);
  }

  function formatPKR(amount) {
    const n = Number(amount || 0);
    return `PKR ${n.toLocaleString("en-PK", { maximumFractionDigits: 0 })}`;
  }

  function statusBadge(status) {
    const safe = (status || "pending").toLowerCase();
    return `<span class="badge badge-${safe}">${safe.replace(/_/g, " ")}</span>`;
  }

  function initials(name) {
    if (!name) return "OR";
    return name
      .split(" ")
      .slice(0, 2)
      .map((p) => p[0] || "")
      .join("")
      .toUpperCase();
  }

  function qs(sel, root = document) {
    return root.querySelector(sel);
  }

  function setLoading(btn, loading) {
    if (!btn) return;
    if (loading) {
      btn.dataset.originalText = btn.textContent;
      btn.disabled = true;
      btn.textContent = "Please wait…";
    } else {
      btn.disabled = false;
      btn.textContent = btn.dataset.originalText || btn.textContent;
    }
  }

  global.ORUI = { toast, formatPKR, statusBadge, initials, qs, setLoading };
})(window);
