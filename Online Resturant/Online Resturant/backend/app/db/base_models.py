"""Import all models so Alembic and metadata discovery see them."""

from app.db.base import Base  # noqa: F401
from app.models.user import User, Role, Permission, RolePermission  # noqa: F401
from app.models.restaurant import Restaurant  # noqa: F401
from app.models.branch import Branch  # noqa: F401
from app.models.staff import Staff  # noqa: F401
from app.models.menu import (  # noqa: F401
    Category,
    MenuItem,
    ItemVariation,
    ItemAddon,
    Deal,
    Combo,
    BranchMenuItem,
)
from app.models.customer import Customer  # noqa: F401
from app.models.order import Order, OrderItem, OrderStatusHistory, Payment  # noqa: F401
from app.models.whatsapp import (  # noqa: F401
    WhatsAppConversation,
    WhatsAppMessage,
    WhatsAppOrderSession,
)
from app.models.ai_call import AICallLog  # noqa: F401
from app.models.crm import CRMNote, Feedback  # noqa: F401
from app.models.subscription import SubscriptionPlan, RestaurantSubscription  # noqa: F401
from app.models.audit import AuditLog, ReportsCache  # noqa: F401
