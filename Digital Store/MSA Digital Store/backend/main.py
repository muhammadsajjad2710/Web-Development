from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import Base, engine
from routers import (
    auth,
    products,
    categories,
    cart,
    orders,
    sellers,
    admin,
    inventory,
    reviews,
    reports,
    wishlist,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MSA Digital Store API",
    description="Marketplace REST API by MSA Technologies",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(sellers.router)
app.include_router(admin.router)
app.include_router(inventory.router)
app.include_router(reviews.router)
app.include_router(reports.router)
app.include_router(wishlist.router)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
ROOT_LOGO = Path(__file__).resolve().parent.parent / "Logo.png"


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "brand": "MSA Digital Store",
        "company": "MSA Technologies",
        "tagline": "Your trusted online shopping destination",
    }


if FRONTEND_DIR.exists():
    app.mount("/css", StaticFiles(directory=FRONTEND_DIR / "css"), name="css")
    app.mount("/js", StaticFiles(directory=FRONTEND_DIR / "js"), name="js")
    app.mount("/images", StaticFiles(directory=FRONTEND_DIR / "images"), name="images")
    app.mount("/admin", StaticFiles(directory=FRONTEND_DIR / "admin", html=True), name="admin")

    @app.get("/")
    def serve_home():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/Logo.png")
    def serve_root_logo():
        path = FRONTEND_DIR / "images" / "Logo.png"
        if path.exists():
            return FileResponse(path)
        if ROOT_LOGO.exists():
            return FileResponse(ROOT_LOGO)
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/{page_name}.html")
    def serve_page(page_name: str):
        path = FRONTEND_DIR / f"{page_name}.html"
        if path.exists():
            return FileResponse(path)
        return FileResponse(FRONTEND_DIR / "index.html")


@app.on_event("startup")
def on_startup():
    try:
        from seed import seed
        seed()
    except Exception as exc:
        print(f"Seed note: {exc}")
