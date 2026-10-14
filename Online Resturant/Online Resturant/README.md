# Online Restaurant

**World-class multi-tenant restaurant management & automation SaaS** by **MSA Technologies**.

Stack: **FastAPI · PostgreSQL · SQLAlchemy · Alembic · JWT/RBAC** on the backend; **HTML · CSS · Vanilla JavaScript** on the frontend (no React/Vue/Angular).

---

## MVP features

- Multi-tenant restaurant registration with **15-day free trial**
- Restaurant profile, branches, digital menu (categories, items, variations, add-ons)
- Public restaurant website (`/r/{slug}` via `pages/restaurant/?slug=…`)
- Online ordering, cart, checkout, order tracking
- Admin dashboard with KPIs, sales chart, recent orders
- Order management with status workflow
- CRM customers, notes, feedback placeholders
- WhatsApp order automation (sandbox / mock-ready)
- AI chat & AI phone call log placeholders (OpenAI / Twilio ready)
- Subscription plans: Basic · Professional · Premium · Enterprise
- Role-based access: Super Admin, Owner, Branch Manager, Kitchen, Order, Delivery, Marketing, Customer

---

## Project structure

```
backend/
  app/
    main.py              # FastAPI entry
    core/                # Config, security, enums, exceptions
    auth/                # JWT deps & RBAC
    api/v1/endpoints/    # Versioned REST APIs
    models/              # SQLAlchemy models
    schemas/             # Pydantic schemas
    services/            # Business logic
    db/                  # Engine, session, model registry
    middleware/
  alembic/               # Migrations
  scripts/               # init_db.py, seed.py
  requirements.txt
  .env.example

frontend/
  index.html             # Landing
  assets/css|js/
  pages/auth/
  pages/dashboard/
  pages/restaurant/
```

---

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Node optional (only if using `npx serve` for static frontend)

---

## Backend setup

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # or: cp .env.example .env
```

Create the database:

```sql
CREATE DATABASE online_restaurant;
```

Update `DATABASE_URL` in `.env`, then:

```bash
# Create tables (dev bootstrap)
python -m scripts.init_db

# Or via Alembic (recommended for production)
# alembic revision --autogenerate -m "initial_schema"
# alembic upgrade head

# Seed demo data
python -m scripts.seed

# Run API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API docs: http://127.0.0.1:8000/docs  
- Health: http://127.0.0.1:8000/health  

### Demo credentials (after seed)

| Role | Email | Password |
|------|-------|----------|
| Super Admin | `admin@msa.tech` | `Admin@12345` |
| Restaurant Owner | `owner@lahorespicehouse.pk` | `Owner@12345` |

Demo public site slug: **`lahore-spice-house`**

---

## Frontend setup

```bash
cd frontend
npx --yes serve -l 5500
```

Open http://127.0.0.1:5500

Ensure CORS in backend `.env` includes your frontend origin (defaults include `5500`).

---

## API overview (`/api/v1`)

| Group | Examples |
|-------|----------|
| Auth | `POST /auth/login`, `/auth/register-restaurant`, `/auth/me` |
| Restaurants | `GET /restaurants/me`, `GET /restaurants/public/{slug}` |
| Branches | `GET|POST /branches` |
| Menu | `GET /menu/items`, `GET /public/{slug}/items` |
| Orders | `GET /orders`, `POST /public/{slug}/orders`, `PATCH /orders/{id}/status` |
| Dashboard | `GET /dashboard/stats` |
| Customers / CRM | `/customers`, `/crm/notes` |
| WhatsApp | `POST /whatsapp/inbound`, `GET /whatsapp/conversations` |
| AI | `POST /ai/chat`, `/ai/calls` |
| Subscriptions | `GET /subscriptions/plans`, `/subscriptions/me` |
| Reports | `GET /reports/summary` |

All tenant-scoped admin endpoints isolate data by the authenticated user's `restaurant_id` (super admins may pass `X-Restaurant-Id`).

---

## User roles

| Role | Access summary |
|------|----------------|
| Platform Super Admin | All restaurants / platform |
| Restaurant Owner | Full restaurant modules |
| Branch Manager | Orders, menu edit, CRM, branch settings |
| Kitchen Staff | View/update kitchen order status |
| Order Staff | Orders + WhatsApp reply |
| Delivery Staff | Delivery status updates |
| Marketing Staff | CRM + reports |
| Customer | Own profile / orders |

---

## Environment variables

See `backend/.env.example` for:

- `SECRET_KEY`, `DATABASE_URL`, JWT TTLs
- `OPENAI_API_KEY` (placeholder)
- WhatsApp / Twilio placeholders
- CORS and trial days

**Never commit real secrets.**

---

## Security

- Bcrypt password hashing
- JWT access + refresh tokens
- RBAC permission matrix
- Restaurant-level data isolation
- Pydantic validation + SQLAlchemy ORM (injection-safe)
- CORS configuration
- Audit log table ready
- Rate-limit structure via config (`RATE_LIMIT_PER_MINUTE`)

---

## Future roadmap

1. Live Meta WhatsApp Cloud API adapter  
2. OpenAI-powered Urdu/English order assistant  
3. Twilio / voice AI phone agent  
4. Payment gateways (JazzCash, EasyPaisa, Stripe)  
5. Real-time WebSocket kitchen boards  
6. Advanced multi-branch inventory  
7. White-label domains per restaurant  
8. Mobile companion apps  

---

## Deployment notes

- Run PostgreSQL managed service; set strong `SECRET_KEY`
- `alembic upgrade head` on deploy
- Serve API behind HTTPS (Uvicorn/Gunicorn + reverse proxy)
- Host frontend on CDN/static hosting; point `FRONTEND_URL` and CORS
- Disable `/docs` in production (`APP_DEBUG=false`)
- Configure object storage for logo/menu images (upload dir ready)

---

## License

Proprietary — MSA Technologies. All rights reserved.
