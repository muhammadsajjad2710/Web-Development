"""Shared enums and constants for Online Restaurant."""

import enum


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    RESTAURANT_OWNER = "restaurant_owner"
    BRANCH_MANAGER = "branch_manager"
    KITCHEN_STAFF = "kitchen_staff"
    ORDER_STAFF = "order_staff"
    DELIVERY_STAFF = "delivery_staff"
    MARKETING_STAFF = "marketing_staff"
    CUSTOMER = "customer"


class RestaurantStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class BranchStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TEMPORARILY_CLOSED = "temporarily_closed"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY_FOR_PICKUP = "ready_for_pickup"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class OrderType(str, enum.Enum):
    DELIVERY = "delivery"
    PICKUP = "pickup"
    DINE_IN = "dine_in"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"
    PARTIAL = "partial"


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
    WALLET = "wallet"
    COD = "cod"


class SubscriptionStatus(str, enum.Enum):
    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class PlanName(str, enum.Enum):
    BASIC = "basic"
    PROFESSIONAL = "professional"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class SpiceLevel(str, enum.Enum):
    NONE = "none"
    MILD = "mild"
    MEDIUM = "medium"
    HOT = "hot"
    EXTRA_HOT = "extra_hot"


class ConversationStatus(str, enum.Enum):
    ACTIVE = "active"
    WAITING = "waiting"
    HUMAN_HANDOVER = "human_handover"
    RESOLVED = "resolved"
    CLOSED = "closed"


class WhatsAppSessionStatus(str, enum.Enum):
    STARTED = "started"
    BROWSING_MENU = "browsing_menu"
    SELECTING_ITEMS = "selecting_items"
    COLLECTING_ADDRESS = "collecting_address"
    CONFIRMING = "confirming"
    ORDER_CREATED = "order_created"
    CANCELLED = "cancelled"
    HANDED_OVER = "handed_over"


class CallStatus(str, enum.Enum):
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    MISSED = "missed"
    FAILED = "failed"
    HUMAN_FOLLOWUP = "human_followup"


class MessageDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Currency(str, enum.Enum):
    PKR = "PKR"
    USD = "USD"
    GBP = "GBP"
    AED = "AED"
    SAR = "SAR"


# Role → default permission keys
ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: ["*"],
    UserRole.RESTAURANT_OWNER: [
        "dashboard:view",
        "orders:*",
        "menu:*",
        "branches:*",
        "staff:*",
        "customers:*",
        "crm:*",
        "reports:*",
        "whatsapp:*",
        "settings:*",
        "subscriptions:view",
    ],
    UserRole.BRANCH_MANAGER: [
        "dashboard:view",
        "orders:*",
        "menu:view",
        "menu:edit",
        "staff:view",
        "customers:*",
        "crm:*",
        "reports:view",
        "whatsapp:view",
        "settings:branch",
    ],
    UserRole.KITCHEN_STAFF: [
        "orders:view",
        "orders:update_status",
        "menu:view",
    ],
    UserRole.ORDER_STAFF: [
        "orders:*",
        "customers:view",
        "menu:view",
        "whatsapp:view",
        "whatsapp:reply",
    ],
    UserRole.DELIVERY_STAFF: [
        "orders:view",
        "orders:update_status",
        "orders:delivery",
    ],
    UserRole.MARKETING_STAFF: [
        "customers:view",
        "crm:*",
        "reports:view",
        "menu:view",
    ],
    UserRole.CUSTOMER: [
        "orders:own",
        "menu:view",
        "profile:own",
    ],
}
