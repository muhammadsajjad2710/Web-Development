"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, menu, misc, orders, restaurants

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(restaurants.router)
api_router.include_router(menu.router)
api_router.include_router(orders.router)
api_router.include_router(misc.dashboard_router)
api_router.include_router(misc.customers_router)
api_router.include_router(misc.crm_router)
api_router.include_router(misc.whatsapp_router)
api_router.include_router(misc.ai_router)
api_router.include_router(misc.subscriptions_router)
api_router.include_router(misc.reports_router)
