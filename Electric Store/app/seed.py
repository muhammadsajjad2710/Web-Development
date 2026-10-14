from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from app.auth import get_password_hash
from app.models import (
    Customer,
    Expense,
    Installment,
    InstallmentPayment,
    Product,
    Sale,
    User,
)


def seed_database(db: Session) -> None:
    if db.query(User).first():
        return

    admin = User(
        username="admin",
        password_hash=get_password_hash("admin123"),
        full_name="Shop Admin",
    )
    db.add(admin)

    products_data = [
        {
            "name": "LED TV 43 inch",
            "description": "Samsung Smart LED TV",
            "quantity": 5,
            "purchase_price": 80000,
            "sale_price": 95000,
            "image_path": "/static/uploads/tv.svg",
        },
        {
            "name": "Refrigerator 14 Cu Ft",
            "description": "Haier Double Door Fridge",
            "quantity": 3,
            "purchase_price": 65000,
            "sale_price": 78000,
            "image_path": "/static/uploads/fridge.svg",
        },
        {
            "name": "Washing Machine 8kg",
            "description": "Automatic Front Load",
            "quantity": 4,
            "purchase_price": 45000,
            "sale_price": 55000,
            "image_path": "/static/uploads/washing.svg",
        },
        {
            "name": "Split AC 1.5 Ton",
            "description": "Inverter AC with warranty",
            "quantity": 2,
            "purchase_price": 120000,
            "sale_price": 145000,
            "image_path": "/static/uploads/ac.svg",
        },
        {
            "name": "Microwave Oven",
            "description": "Digital microwave 30L",
            "quantity": 8,
            "purchase_price": 15000,
            "sale_price": 18500,
            "image_path": "/static/uploads/microwave.svg",
        },
    ]

    products = []
    for data in products_data:
        product = Product(**data)
        db.add(product)
        products.append(product)
    db.flush()

    customers_data = [
        {
            "name": "Ali Ahmed",
            "phone": "0300-1234567",
            "cnic": "35202-1234567-1",
            "address": "Gulberg, Lahore",
        },
        {
            "name": "Fatima Khan",
            "phone": "0321-9876543",
            "cnic": "35202-7654321-2",
            "address": "Model Town, Lahore",
        },
        {
            "name": "Usman Malik",
            "phone": "0333-5551234",
            "cnic": "35202-9876543-3",
            "address": "Johar Town, Lahore",
        },
    ]

    customers = []
    for data in customers_data:
        customer = Customer(**data)
        db.add(customer)
        customers.append(customer)
    db.flush()

    # Cash sale today
    cash_sale = Sale(
        invoice_no="INV-1001",
        product_id=products[4].id,
        customer_id=customers[1].id,
        sale_type="cash",
        quantity=1,
        unit_price=products[4].sale_price,
        total_amount=products[4].sale_price,
        down_payment=products[4].sale_price,
        remaining_amount=0,
        sale_date=datetime.combine(date.today(), datetime.now().time()),
    )
    db.add(cash_sale)
    products[4].quantity -= 1

    # Installment sale 1 - Ali bought Fridge
    fridge = products[1]
    total = fridge.sale_price
    down = 18000
    remaining = total - down
    monthly = 5000
    months = int(remaining / monthly)

    sale1 = Sale(
        invoice_no="INV-1002",
        product_id=fridge.id,
        customer_id=customers[0].id,
        sale_type="installment",
        quantity=1,
        unit_price=fridge.sale_price,
        total_amount=total,
        down_payment=down,
        remaining_amount=remaining,
        sale_date=datetime.utcnow() - timedelta(days=45),
    )
    db.add(sale1)
    db.flush()
    fridge.quantity -= 1

    inst1 = Installment(
        sale_id=sale1.id,
        customer_id=customers[0].id,
        product_id=fridge.id,
        total_amount=total,
        down_payment=down,
        remaining_balance=remaining - 10000,
        monthly_amount=monthly,
        total_months=months,
        start_date=date.today() - timedelta(days=45),
        next_due_date=date.today() + timedelta(days=5),
        status="active",
    )
    db.add(inst1)
    db.flush()

    db.add(
        InstallmentPayment(
            installment_id=inst1.id,
            amount=5000,
            payment_date=date.today() - timedelta(days=15),
            status="paid",
        )
    )
    db.add(
        InstallmentPayment(
            installment_id=inst1.id,
            amount=5000,
            payment_date=date.today() - timedelta(days=45),
            status="paid",
        )
    )

    # Installment sale 2 - Usman bought AC
    ac = products[3]
    total2 = ac.sale_price
    down2 = 45000
    remaining2 = total2 - down2
    monthly2 = 10000

    sale2 = Sale(
        invoice_no="INV-1003",
        product_id=ac.id,
        customer_id=customers[2].id,
        sale_type="installment",
        quantity=1,
        unit_price=ac.sale_price,
        total_amount=total2,
        down_payment=down2,
        remaining_amount=remaining2,
        sale_date=datetime.utcnow() - timedelta(days=20),
    )
    db.add(sale2)
    db.flush()
    ac.quantity -= 1

    inst2 = Installment(
        sale_id=sale2.id,
        customer_id=customers[2].id,
        product_id=ac.id,
        total_amount=total2,
        down_payment=down2,
        remaining_balance=remaining2,
        monthly_amount=monthly2,
        total_months=int(remaining2 / monthly2),
        start_date=date.today() - timedelta(days=20),
        next_due_date=date.today() - timedelta(days=2),
        status="overdue",
    )
    db.add(inst2)

    expenses_data = [
        {"category": "Rent", "description": "Shop rent - June", "amount": 25000},
        {"category": "Bills", "description": "Electricity bill", "amount": 8500},
        {"category": "Salaries", "description": "Staff salary", "amount": 18000},
    ]
    for data in expenses_data:
        db.add(Expense(expense_date=date.today().replace(day=1), **data))

    db.commit()
