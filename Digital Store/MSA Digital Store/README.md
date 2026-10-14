# MSA Digital Store MVP

Premium e-commerce marketplace by **MSA Technologies**.

**Stack:** FastAPI + SQLAlchemy + SQLite · Vanilla HTML/CSS/JavaScript

## Quick start

```bash
cd backend
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open: **http://127.0.0.1:8000/**

API docs: **http://127.0.0.1:8000/docs**

## Demo accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@msadigitalstore.pk | admin123 |
| Customer | customer@msa.local | customer123 |
| Seller | seller@msatechnologies.pk | seller123 |

## Features

- Product catalogue (24 seeded products), categories, search & filters
- Cart (guest localStorage + authenticated API cart)
- Checkout & order placement with stock reduction
- Order tracking timeline
- Seller registration
- JWT auth (customer / seller / admin)
- Admin dashboard: products, orders, inventory, sellers, reports

## Project layout

```
backend/     FastAPI app, models, routers, seed
frontend/    HTML pages, css/, js/, admin/
```

## Brand

- Navy header/footer · Teal accents · Gold badges
- Tagline: *Your trusted online shopping destination*
- Vision: *Starting local. Scaling national. Reaching global.*
