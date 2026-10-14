"""Dashboard, customers, CRM, WhatsApp, AI, subscriptions, reports endpoints."""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth.deps import (
    get_current_user,
    get_restaurant_id_header,
    require_restaurant_access,
    resolve_tenant_id,
    user_has_permission,
)
from app.core.exceptions import ForbiddenError
from app.db.session import get_db
from app.models.subscription import RestaurantSubscription, SubscriptionPlan
from app.models.user import User
from app.schemas import (
    AICallLogCreate,
    AICallLogOut,
    AIChatRequest,
    AIChatResponse,
    CRMNoteCreate,
    CRMNoteOut,
    CustomerCreate,
    CustomerOut,
    CustomerUpdate,
    DashboardStats,
    FeedbackCreate,
    HumanHandoverRequest,
    RestaurantSubscriptionOut,
    SubscriptionPlanOut,
    WhatsAppConversationOut,
    WhatsAppInboundMessage,
    WhatsAppMessageOut,
)
from app.schemas.common import MessageResponse, PaginatedResponse
from app.services.ai_service import AIAssistantService, AICallService
from app.services.customer_service import CustomerService
from app.services.dashboard_service import DashboardService
from app.services.whatsapp_service import WhatsAppService

dashboard_router = APIRouter(prefix="/dashboard", tags=["dashboard"])
customers_router = APIRouter(prefix="/customers", tags=["customers"])
crm_router = APIRouter(prefix="/crm", tags=["crm"])
whatsapp_router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])
ai_router = APIRouter(prefix="/ai", tags=["ai"])
subscriptions_router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])
reports_router = APIRouter(prefix="/reports", tags=["reports"])


def _tenant(user: User, header_id: Optional[UUID]) -> UUID:
    tenant = resolve_tenant_id(user, header_id)
    if not tenant:
        raise ForbiddenError("Restaurant context required")
    return tenant


@dashboard_router.get("/stats", response_model=DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "dashboard:view"):
        raise ForbiddenError("Missing dashboard permission")
    return DashboardService(db).get_stats(_tenant(user, header_id))


@customers_router.get("", response_model=PaginatedResponse[CustomerOut])
def list_customers(
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "customers:*") and not user_has_permission(
        user, "customers:view"
    ):
        raise ForbiddenError("Missing customers permission")
    items, meta = CustomerService(db).list(
        _tenant(user, header_id), search=search, page=page, page_size=page_size
    )
    return PaginatedResponse(items=[CustomerOut.model_validate(i) for i in items], **meta)


@customers_router.post("", response_model=CustomerOut, status_code=201)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "customers:*"):
        raise ForbiddenError("Missing customers permission")
    return CustomerService(db).create(_tenant(user, header_id), payload)


@customers_router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return CustomerService(db).get(_tenant(user, header_id), customer_id)


@customers_router.patch("/{customer_id}", response_model=CustomerOut)
def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "customers:*"):
        raise ForbiddenError("Missing customers permission")
    return CustomerService(db).update(_tenant(user, header_id), customer_id, payload)


@crm_router.post("/notes", response_model=CRMNoteOut, status_code=201)
def create_crm_note(
    payload: CRMNoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "crm:*"):
        raise ForbiddenError("Missing CRM permission")
    return CustomerService(db).add_note(_tenant(user, header_id), payload, user.id)


@crm_router.get("/notes", response_model=List[CRMNoteOut])
def list_crm_notes(
    customer_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "crm:*"):
        raise ForbiddenError("Missing CRM permission")
    return CustomerService(db).list_notes(_tenant(user, header_id), customer_id)


@crm_router.post("/feedback", response_model=MessageResponse, status_code=201)
def create_feedback(
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    CustomerService(db).add_feedback(_tenant(user, header_id), payload)
    return MessageResponse(message="Feedback recorded")


@whatsapp_router.get("/conversations", response_model=List[WhatsAppConversationOut])
def list_whatsapp_conversations(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "whatsapp:*") and not user_has_permission(
        user, "whatsapp:view"
    ):
        raise ForbiddenError("Missing WhatsApp permission")
    return WhatsAppService(db).list_conversations(_tenant(user, header_id))


@whatsapp_router.get(
    "/conversations/{conversation_id}/messages", response_model=List[WhatsAppMessageOut]
)
def list_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    conversation = WhatsAppService(db).get_conversation(
        _tenant(user, header_id), conversation_id
    )
    return conversation.messages


@whatsapp_router.post("/inbound", response_model=WhatsAppMessageOut)
def whatsapp_inbound(payload: WhatsAppInboundMessage, db: Session = Depends(get_db)):
    """Sandbox webhook for inbound WhatsApp messages (no live Meta API required)."""
    _, outbound, _ = WhatsAppService(db).handle_inbound(payload)
    return outbound


@whatsapp_router.post(
    "/conversations/{conversation_id}/handover", response_model=WhatsAppConversationOut
)
def human_handover(
    conversation_id: UUID,
    payload: HumanHandoverRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "whatsapp:*") and not user_has_permission(
        user, "whatsapp:reply"
    ):
        raise ForbiddenError("Missing WhatsApp permission")
    return WhatsAppService(db).set_human_handover(
        _tenant(user, header_id),
        conversation_id,
        payload.enabled,
        payload.staff_id or user.id,
    )


@ai_router.post("/chat", response_model=AIChatResponse)
def ai_chat(payload: AIChatRequest):
    return AIAssistantService().chat(payload)


@ai_router.post("/calls", response_model=AICallLogOut, status_code=201)
def create_call_log(
    payload: AICallLogCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return AICallService(db).create_log(payload)


@ai_router.get("/calls", response_model=List[AICallLogOut])
def list_call_logs(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    return AICallService(db).list_logs(_tenant(user, header_id))


@subscriptions_router.get("/plans", response_model=List[SubscriptionPlanOut])
def list_plans(db: Session = Depends(get_db)):
    return (
        db.query(SubscriptionPlan)
        .filter(SubscriptionPlan.is_active.is_(True))
        .order_by(SubscriptionPlan.sort_order)
        .all()
    )


@subscriptions_router.get("/me", response_model=RestaurantSubscriptionOut)
def my_subscription(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    from sqlalchemy.orm import joinedload

    sub = (
        db.query(RestaurantSubscription)
        .options(joinedload(RestaurantSubscription.plan))
        .filter(RestaurantSubscription.restaurant_id == _tenant(user, header_id))
        .first()
    )
    if not sub:
        raise ForbiddenError("No subscription found")
    return sub


@reports_router.get("/summary")
def reports_summary(
    db: Session = Depends(get_db),
    user: User = Depends(require_restaurant_access),
    header_id: Optional[UUID] = Depends(get_restaurant_id_header),
):
    if not user_has_permission(user, "reports:*") and not user_has_permission(
        user, "reports:view"
    ):
        raise ForbiddenError("Missing reports permission")
    stats = DashboardService(db).get_stats(_tenant(user, header_id))
    return {
        "success": True,
        "daily_sales": stats.sales_by_day,
        "total_revenue": float(stats.total_revenue),
        "total_orders": stats.total_orders,
        "top_items": stats.top_selling_items,
        "repeat_customers": stats.repeat_customers,
        "cancelled_orders": stats.cancelled_orders,
        "customer_growth": stats.customer_count,
        "orders_by_status": stats.orders_by_status,
    }
