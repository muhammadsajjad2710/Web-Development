# Electric Store — Shop Management Demo

A lightweight **FastAPI + Bootstrap** demo for a single electronics/electric shop. Includes inventory, sales, installments, expenses, and a dashboard with charts.

## Features

- **JWT Login** — Secure admin authentication
- **Dashboard** — Today sales, products, installments due, profit, charts
- **Products** — Add/edit/delete with image upload and stock alerts
- **Customers** — Name, phone, CNIC, address
- **Sales** — Cash and installment sales with auto invoice numbers
- **Installments** — Remaining balance tracking and payment recording
- **Expenses** — Rent, bills, salaries, repairs

## Demo Data (pre-loaded)

| Item | Details |
|------|---------|
| **Login** | `admin` / `admin123` |
| **Products** | 5 items (TV, Fridge, Washing Machine, AC, Microwave) |
| **Customers** | 3 customers |
| **Installments** | 2 active records (Ali — Fridge, Usman — AC) |
| **Expenses** | Rent, bills, salaries |

## Quick Start

### 1. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Open in browser

```
http://localhost:8000
```

Login with **admin** / **admin123**

## Project Structure

```
Electric Store/
├── app/
│   ├── main.py           # FastAPI app & page routes
│   ├── config.py         # Settings
│   ├── database.py       # SQLAlchemy setup
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── auth.py           # JWT authentication
│   ├── seed.py           # Demo sample data
│   └── routers/          # API endpoints
├── templates/            # HTML pages (Jinja2)
├── static/
│   ├── css/style.css
│   ├── js/               # Frontend JavaScript
│   └── uploads/          # Product images
├── requirements.txt
└── .env.example
```

## Database

**Demo mode** uses SQLite (`electric_store.db`) — no setup required.

For **MySQL** in production, copy `.env.example` to `.env`:

```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/electric_store
```

Create the database first:

```sql
CREATE DATABASE electric_store CHARACTER SET utf8mb4;
```

## API Documentation

When the server is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Roadmap (Future Phases)

- Phase 2: Reports, PDF invoices, advanced charts
- Phase 3: WhatsApp/SMS reminders, barcode scanner, thermal printing, cloud backup

## License

Demo project for shop presentation.
