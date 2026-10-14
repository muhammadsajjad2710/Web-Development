# Online Restaurant Frontend

Vanilla HTML/CSS/JavaScript client for the Online Restaurant SaaS platform by **MSA Technologies**.

## Pages

- `index.html` — Marketing landing
- `pages/auth/` — Login, register, forgot password
- `pages/dashboard/` — Admin shell (orders, menu, CRM, WhatsApp, reports, settings…)
- `pages/restaurant/` — Public restaurant site (`?slug=lahore-spice-house`)

## Run locally

Serve the `frontend` folder with any static server, for example:

```bash
npx --yes serve -l 5500
```

Or open files via Live Server in VS Code/Cursor (port 5500 recommended).

API base URL defaults to `http://127.0.0.1:8000/api/v1` (see `assets/js/api.js`).
