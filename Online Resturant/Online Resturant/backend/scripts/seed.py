"""
Database seed script — demo Pakistani restaurant data.

Usage (from backend/):
  python -m scripts.seed
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

# Ensure backend root is on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy.orm import Session

from app.core.enums import PlanName, SubscriptionStatus, UserRole
from app.core.security import hash_password
from app.db.base import Base
from app.db.session import SessionLocal, engine
import app.db.base_models  # noqa: F401
from app.models.branch import Branch
from app.models.customer import Customer
from app.models.menu import Category, ItemAddon, ItemVariation, MenuItem
from app.models.order import Order, OrderItem, OrderStatusHistory, Payment
from app.models.restaurant import Restaurant
from app.models.subscription import RestaurantSubscription, SubscriptionPlan
from app.models.user import Permission, Role, RolePermission, User
from app.utils.helpers import generate_order_number, slugify


ROLES = [
    (UserRole.SUPER_ADMIN.value, "Platform Super Admin", "Full platform access"),
    (UserRole.RESTAURANT_OWNER.value, "Restaurant Owner", "Owns and manages a restaurant"),
    (UserRole.BRANCH_MANAGER.value, "Branch Manager", "Manages a single branch"),
    (UserRole.KITCHEN_STAFF.value, "Kitchen Staff", "Kitchen order preparation"),
    (UserRole.ORDER_STAFF.value, "Order Staff", "Handles incoming orders"),
    (UserRole.DELIVERY_STAFF.value, "Delivery Staff", "Delivery riders"),
    (UserRole.MARKETING_STAFF.value, "Marketing Staff", "CRM and campaigns"),
    (UserRole.CUSTOMER.value, "Customer", "End customer"),
]

PERMISSIONS = [
    ("dashboard:view", "View Dashboard", "dashboard"),
    ("orders:view", "View Orders", "orders"),
    ("orders:update_status", "Update Order Status", "orders"),
    ("orders:delivery", "Manage Delivery", "orders"),
    ("orders:*", "Full Orders Access", "orders"),
    ("menu:view", "View Menu", "menu"),
    ("menu:edit", "Edit Menu", "menu"),
    ("menu:*", "Full Menu Access", "menu"),
    ("branches:*", "Manage Branches", "branches"),
    ("staff:*", "Manage Staff", "staff"),
    ("staff:view", "View Staff", "staff"),
    ("customers:view", "View Customers", "customers"),
    ("customers:*", "Manage Customers", "customers"),
    ("crm:*", "CRM Access", "crm"),
    ("reports:view", "View Reports", "reports"),
    ("reports:*", "Full Reports", "reports"),
    ("whatsapp:view", "View WhatsApp", "whatsapp"),
    ("whatsapp:reply", "Reply WhatsApp", "whatsapp"),
    ("whatsapp:*", "Full WhatsApp", "whatsapp"),
    ("settings:*", "Full Settings", "settings"),
    ("settings:branch", "Branch Settings", "settings"),
    ("subscriptions:view", "View Subscription", "subscriptions"),
    ("orders:own", "Own Orders", "orders"),
    ("profile:own", "Own Profile", "users"),
]

PLANS = [
    {
        "name": PlanName.BASIC.value,
        "display_name": "Basic",
        "description": "Single branch starter plan",
        "price_monthly": Decimal("4999.00"),
        "price_yearly": Decimal("49990.00"),
        "max_branches": 1,
        "max_staff": 5,
        "max_menu_items": 50,
        "features": {
            "website": True,
            "online_ordering": True,
            "whatsapp": False,
            "ai_chat": False,
            "ai_phone": False,
            "reports": "basic",
        },
        "sort_order": 1,
    },
    {
        "name": PlanName.PROFESSIONAL.value,
        "display_name": "Professional",
        "description": "Growing restaurants with WhatsApp automation",
        "price_monthly": Decimal("9999.00"),
        "price_yearly": Decimal("99990.00"),
        "max_branches": 3,
        "max_staff": 20,
        "max_menu_items": 200,
        "features": {
            "website": True,
            "online_ordering": True,
            "whatsapp": True,
            "ai_chat": True,
            "ai_phone": False,
            "reports": "advanced",
        },
        "sort_order": 2,
    },
    {
        "name": PlanName.PREMIUM.value,
        "display_name": "Premium",
        "description": "Multi-branch with AI assistants",
        "price_monthly": Decimal("19999.00"),
        "price_yearly": Decimal("199990.00"),
        "max_branches": 10,
        "max_staff": 50,
        "max_menu_items": 500,
        "features": {
            "website": True,
            "online_ordering": True,
            "whatsapp": True,
            "ai_chat": True,
            "ai_phone": True,
            "reports": "premium",
        },
        "sort_order": 3,
    },
    {
        "name": PlanName.ENTERPRISE.value,
        "display_name": "Enterprise",
        "description": "Unlimited scale with dedicated support",
        "price_monthly": Decimal("49999.00"),
        "price_yearly": Decimal("499990.00"),
        "max_branches": 999,
        "max_staff": 999,
        "max_menu_items": 9999,
        "features": {
            "website": True,
            "online_ordering": True,
            "whatsapp": True,
            "ai_chat": True,
            "ai_phone": True,
            "reports": "enterprise",
            "dedicated_support": True,
        },
        "sort_order": 4,
    },
]

MENU = [
    ("BBQ", [
        ("Chicken Karahi", "Traditional chicken karahi with tomatoes and green chillies", "1800.00", "1600.00", True, True, "hot", "Full"),
        ("Chicken Tikka", "Charcoal grilled chicken tikka pieces", "900.00", None, True, False, "medium", "6 pcs"),
        ("BBQ Platter", "Mixed BBQ platter for sharing", "3200.00", "2999.00", True, True, "medium", "Family"),
    ]),
    ("Rice", [
        ("Chicken Biryani", "Hyderabadi-style chicken biryani", "450.00", None, True, True, "medium", "Single"),
        ("Beef Biryani", "Slow-cooked beef biryani", "550.00", None, False, False, "hot", "Single"),
    ]),
    ("Fast Food", [
        ("Zinger Burger", "Crispy zinger burger with fries option", "550.00", "499.00", True, True, "mild", "Single"),
        ("Chicken Pizza", "12-inch chicken tikka pizza", "1400.00", None, True, False, "mild", "12 inch"),
        ("Loaded Fries", "Cheese and spicy sauce loaded fries", "450.00", None, False, False, "mild", "Regular"),
    ]),
    ("Breads & Drinks", [
        ("Garlic Naan", "Fresh tandoor garlic naan", "80.00", None, False, False, "none", "1 pc"),
        ("Cold Drink", "Chilled soft drink 500ml", "100.00", None, False, False, "none", "500ml"),
    ]),
]


def seed_roles_and_permissions(db: Session) -> dict[str, Role]:
    perm_map: dict[str, Permission] = {}
    for code, name, module in PERMISSIONS:
        perm = db.query(Permission).filter(Permission.code == code).first()
        if not perm:
            perm = Permission(code=code, name=name, module=module)
            db.add(perm)
            db.flush()
        perm_map[code] = perm

    role_map: dict[str, Role] = {}
    for name, display, desc in ROLES:
        role = db.query(Role).filter(Role.name == name).first()
        if not role:
            role = Role(name=name, display_name=display, description=desc, is_system=True)
            db.add(role)
            db.flush()
        role_map[name] = role

    db.commit()
    return role_map


def seed_plans(db: Session) -> dict[str, SubscriptionPlan]:
    plans = {}
    for plan_data in PLANS:
        plan = db.query(SubscriptionPlan).filter(SubscriptionPlan.name == plan_data["name"]).first()
        if not plan:
            plan = SubscriptionPlan(**plan_data, currency="PKR", is_active=True)
            db.add(plan)
            db.flush()
        plans[plan.name] = plan
    db.commit()
    return plans


def seed_demo(db: Session, roles: dict[str, Role], plans: dict[str, SubscriptionPlan]) -> None:
    if db.query(Restaurant).filter(Restaurant.slug == "lahore-spice-house").first():
        print("Demo restaurant already exists — skipping demo seed.")
        return

    restaurant = Restaurant(
        name="Lahore Spice House",
        slug="lahore-spice-house",
        description=(
            "Authentic Pakistani BBQ, karahi, and biryani. "
            "Order online for delivery or pickup across Lahore."
        ),
        cuisine_type="Pakistani, BBQ, Fast Food",
        contact_number="+92-300-1234567",
        whatsapp_number="+92-300-1234567",
        email="demo@lahorespicehouse.pk",
        address="MM Alam Road, Gulberg III, Lahore",
        city="Lahore",
        country="Pakistan",
        currency="PKR",
        status="active",
        tax_rate=Decimal("5.00"),
        service_charge_rate=Decimal("0.00"),
        delivery_available=True,
        pickup_available=True,
        dine_in_available=True,
        opening_hours={
            "monday": {"open": "12:00", "close": "23:30"},
            "tuesday": {"open": "12:00", "close": "23:30"},
            "wednesday": {"open": "12:00", "close": "23:30"},
            "thursday": {"open": "12:00", "close": "23:30"},
            "friday": {"open": "12:00", "close": "00:00"},
            "saturday": {"open": "12:00", "close": "00:00"},
            "sunday": {"open": "13:00", "close": "23:00"},
        },
    )
    db.add(restaurant)
    db.flush()

    owner = User(
        email="owner@lahorespicehouse.pk",
        phone="+92-300-1234567",
        password_hash=hash_password("Owner@12345"),
        full_name="Ahmed Khan",
        role_id=roles[UserRole.RESTAURANT_OWNER.value].id,
        restaurant_id=restaurant.id,
        is_active=True,
        is_verified=True,
    )
    db.add(owner)
    db.flush()
    restaurant.owner_id = owner.id

    admin = User(
        email="admin@msa.tech",
        phone="+92-300-0000001",
        password_hash=hash_password("Admin@12345"),
        full_name="MSA Super Admin",
        role_id=roles[UserRole.SUPER_ADMIN.value].id,
        is_active=True,
        is_verified=True,
    )
    db.add(admin)

    branch = Branch(
        restaurant_id=restaurant.id,
        name="Gulberg Branch",
        address="MM Alam Road, Gulberg III, Lahore",
        contact_number="+92-300-1234567",
        whatsapp_number="+92-300-1234567",
        city="Lahore",
        status="active",
        is_default=True,
        manager_id=owner.id,
        delivery_radius_km=Decimal("8.00"),
    )
    db.add(branch)
    db.flush()

    now = datetime.now(timezone.utc)
    db.add(
        RestaurantSubscription(
            restaurant_id=restaurant.id,
            plan_id=plans[PlanName.PROFESSIONAL.value].id,
            status=SubscriptionStatus.TRIAL.value,
            trial_start=now,
            trial_end=now + timedelta(days=15),
            billing_cycle="monthly",
        )
    )

    item_ids = []
    sort = 0
    for cat_name, items in MENU:
        sort += 1
        category = Category(
            restaurant_id=restaurant.id,
            name=cat_name,
            slug=slugify(cat_name),
            sort_order=sort,
            is_active=True,
        )
        db.add(category)
        db.flush()

        for name, desc, price, discount, popular, featured, spice, serving in items:
            item = MenuItem(
                restaurant_id=restaurant.id,
                category_id=category.id,
                name=name,
                slug=slugify(name),
                description=desc,
                price=Decimal(price),
                discount_price=Decimal(discount) if discount else None,
                preparation_time_minutes=25,
                is_available=True,
                is_popular=popular,
                is_featured=featured,
                spice_level=spice,
                serving_size=serving,
            )
            db.add(item)
            db.flush()
            item_ids.append(item)

            if "Burger" in name:
                db.add(ItemVariation(menu_item_id=item.id, name="Regular", price_delta=Decimal("0"), is_default=True))
                db.add(ItemVariation(menu_item_id=item.id, name="With Fries", price_delta=Decimal("150")))
                db.add(ItemAddon(menu_item_id=item.id, name="Extra Cheese", price=Decimal("80")))
                db.add(ItemAddon(menu_item_id=item.id, name="Spicy Mayo", price=Decimal("40")))

    customers = [
        Customer(
            restaurant_id=restaurant.id,
            full_name="Sara Ali",
            phone="+92-321-1112233",
            email="sara@example.com",
            address="DHA Phase 5, Lahore",
            city="Lahore",
            total_orders=2,
            total_spent=Decimal("2450.00"),
            loyalty_points=120,
            last_order_at=now - timedelta(days=1),
        ),
        Customer(
            restaurant_id=restaurant.id,
            full_name="Usman Raza",
            phone="+92-333-4445566",
            email="usman@example.com",
            address="Johar Town, Lahore",
            city="Lahore",
            total_orders=1,
            total_spent=Decimal("1600.00"),
            loyalty_points=50,
            last_order_at=now - timedelta(hours=5),
        ),
        Customer(
            restaurant_id=restaurant.id,
            full_name="Fatima Noor",
            phone="+92-300-7778899",
            address="Model Town, Lahore",
            city="Lahore",
            total_orders=3,
            total_spent=Decimal("5200.00"),
            loyalty_points=260,
            last_order_at=now - timedelta(days=3),
        ),
    ]
    for c in customers:
        db.add(c)
    db.flush()

    # Sample orders
    sample_orders = [
        (customers[0], "pending", "delivery", [("Chicken Karahi", "1600.00", 1), ("Naan", "80.00", 2)]),
        (customers[1], "preparing", "pickup", [("Chicken Biryani", "450.00", 2), ("Cold Drink", "100.00", 2)]),
        (customers[2], "completed", "delivery", [("Zinger Burger", "499.00", 2), ("Loaded Fries", "450.00", 1)]),
        (customers[0], "out_for_delivery", "delivery", [("BBQ Platter", "2999.00", 1)]),
        (customers[2], "cancelled", "delivery", [("Chicken Pizza", "1400.00", 1)]),
    ]

    for customer, status, otype, lines in sample_orders:
        subtotal = sum(Decimal(p) * q for _, p, q in lines)
        tax = (subtotal * Decimal("0.05")).quantize(Decimal("0.01"))
        delivery = Decimal("100.00") if otype == "delivery" else Decimal("0")
        total = subtotal + tax + delivery
        order = Order(
            restaurant_id=restaurant.id,
            branch_id=branch.id,
            customer_id=customer.id,
            order_number=generate_order_number(),
            order_type=otype,
            status=status,
            payment_status="paid" if status == "completed" else "pending",
            payment_method="cod",
            customer_name=customer.full_name,
            customer_phone=customer.phone,
            customer_email=customer.email,
            delivery_address=customer.address if otype == "delivery" else None,
            subtotal=subtotal,
            tax_amount=tax,
            service_charge=Decimal("0"),
            delivery_fee=delivery,
            discount_amount=Decimal("0"),
            total_amount=total,
            currency="PKR",
            source="website",
            completed_at=now - timedelta(days=2) if status == "completed" else None,
            cancelled_at=now - timedelta(hours=2) if status == "cancelled" else None,
        )
        db.add(order)
        db.flush()
        for name, price, qty in lines:
            unit = Decimal(price)
            db.add(
                OrderItem(
                    order_id=order.id,
                    item_name=name,
                    quantity=qty,
                    unit_price=unit,
                    total_price=unit * qty,
                )
            )
        db.add(
            OrderStatusHistory(
                order_id=order.id,
                from_status=None,
                to_status=status,
                note="Seeded order",
            )
        )
        db.add(
            Payment(
                order_id=order.id,
                restaurant_id=restaurant.id,
                amount=total,
                currency="PKR",
                method="cod",
                status="paid" if status == "completed" else "pending",
            )
        )

    db.commit()
    print("Seed completed successfully.")
    print("  Super Admin : admin@msa.tech / Admin@12345")
    print("  Owner       : owner@lahorespicehouse.pk / Owner@12345")
    print("  Restaurant  : /r/lahore-spice-house")


def main() -> None:
    print("Creating tables if needed...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        roles = seed_roles_and_permissions(db)
        plans = seed_plans(db)
        seed_demo(db, roles, plans)
    finally:
        db.close()


if __name__ == "__main__":
    main()
