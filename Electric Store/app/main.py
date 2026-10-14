import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import UPLOAD_DIR
from app.database import Base, SessionLocal, engine
from app.routers import auth, customers, dashboard, expenses, installments, products, sales
from app.seed import seed_database

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Electric Store POS", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(products.router)
app.include_router(customers.router)
app.include_router(sales.router)
app.include_router(installments.router)
app.include_router(expenses.router)


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "page": "dashboard"})


@app.get("/products", response_class=HTMLResponse)
def products_page(request: Request):
    return templates.TemplateResponse("products.html", {"request": request, "page": "products"})


@app.get("/customers", response_class=HTMLResponse)
def customers_page(request: Request):
    return templates.TemplateResponse("customers.html", {"request": request, "page": "customers"})


@app.get("/sales", response_class=HTMLResponse)
def sales_page(request: Request):
    return templates.TemplateResponse("sales.html", {"request": request, "page": "sales"})


@app.get("/installments", response_class=HTMLResponse)
def installments_page(request: Request):
    return templates.TemplateResponse("installments.html", {"request": request, "page": "installments"})


@app.get("/expenses", response_class=HTMLResponse)
def expenses_page(request: Request):
    return templates.TemplateResponse("expenses.html", {"request": request, "page": "expenses"})
