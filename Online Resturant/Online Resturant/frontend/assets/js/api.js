/**
 * Online Restaurant — Central API client
 */
(function (global) {
  const DEFAULT_BASE = "http://127.0.0.1:8001/api/v1";

  function getBaseUrl() {
    return localStorage.getItem("or_api_base") || DEFAULT_BASE;
  }

  function getTokens() {
    try {
      return JSON.parse(localStorage.getItem("or_tokens") || "null");
    } catch {
      return null;
    }
  }

  function setTokens(tokens) {
    if (!tokens) localStorage.removeItem("or_tokens");
    else localStorage.setItem("or_tokens", JSON.stringify(tokens));
  }

  function getUser() {
    try {
      return JSON.parse(localStorage.getItem("or_user") || "null");
    } catch {
      return null;
    }
  }

  function setUser(user) {
    if (!user) localStorage.removeItem("or_user");
    else localStorage.setItem("or_user", JSON.stringify(user));
  }

  function clearSession() {
    setTokens(null);
    setUser(null);
  }

  async function request(path, options = {}) {
    const tokens = getTokens();
    const headers = {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(options.headers || {}),
    };
    if (tokens?.access_token && !options.skipAuth) {
      headers.Authorization = `Bearer ${tokens.access_token}`;
    }
    if (options.restaurantId) {
      headers["X-Restaurant-Id"] = options.restaurantId;
    }

    const res = await fetch(`${getBaseUrl()}${path}`, {
      method: options.method || "GET",
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
    });

    let data = null;
    const text = await res.text();
    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = { message: text };
      }
    }

    if (!res.ok) {
      const message =
        data?.error?.message || data?.detail || data?.message || `Request failed (${res.status})`;
      const err = new Error(message);
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  }

  const api = {
    getBaseUrl,
    setBaseUrl(url) {
      localStorage.setItem("or_api_base", url);
    },
    getTokens,
    setTokens,
    getUser,
    setUser,
    clearSession,
    isAuthenticated() {
      return Boolean(getTokens()?.access_token);
    },
    requireAuth(redirectTo) {
      if (!this.isAuthenticated()) {
        window.location.href = redirectTo || "../auth/login.html";
        return false;
      }
      return true;
    },
    async login(email, password) {
      const data = await request("/auth/login", {
        method: "POST",
        body: { email, password },
        skipAuth: true,
      });
      setTokens(data.tokens);
      setUser(data.user);
      return data;
    },
    async registerRestaurant(payload) {
      const data = await request("/auth/register-restaurant", {
        method: "POST",
        body: payload,
        skipAuth: true,
      });
      setTokens(data.tokens);
      setUser(data.user);
      return data;
    },
    async me() {
      const user = await request("/auth/me");
      setUser(user);
      return user;
    },
    logout() {
      clearSession();
      window.location.href = "/pages/auth/login.html".replace(/^\//, "") || "../auth/login.html";
    },
    get: (path, opts) => request(path, { ...opts, method: "GET" }),
    post: (path, body, opts) => request(path, { ...opts, method: "POST", body }),
    patch: (path, body, opts) => request(path, { ...opts, method: "PATCH", body }),
    del: (path, opts) => request(path, { ...opts, method: "DELETE" }),
  };

  global.ORApi = api;
})(window);
