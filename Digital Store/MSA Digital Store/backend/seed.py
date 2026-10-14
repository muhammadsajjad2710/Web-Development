"""Seed database with admin, sellers, categories, and 24 products."""
from database import SessionLocal, engine, Base
from models import (
    User,
    UserRole,
    Customer,
    Seller,
    SellerStatus,
    SellingType,
    Category,
    Product,
    ProductImage,
    ProductBadge,
    StockStatus,
    Inventory,
)
from auth import get_password_hash
from routers.products import compute_stock_status, slugify


CATEGORIES = [
    ("Electronics", "electronics", "Gadgets, devices & tech essentials", "cpu"),
    ("Mobile Accessories", "mobile-accessories", "Cables, cases, earbuds & more", "smartphone"),
    ("Fashion", "fashion", "Clothing, bags & style", "shirt"),
    ("Shoes", "shoes", "Footwear for every occasion", "footprints"),
    ("Beauty Products", "beauty-products", "Skincare, fragrance & grooming", "sparkles"),
    ("Groceries", "groceries", "Everyday essentials & packs", "basket"),
    ("Home & Kitchen", "home-kitchen", "Appliances & home comfort", "home"),
    ("Baby Products", "baby-products", "Care packs for little ones", "baby"),
    ("Books & Stationery", "books-stationery", "Learning & office supplies", "book"),
    ("Daily Use Items", "daily-use-items", "Cleaning & household needs", "package"),
]

SELLERS = [
    {
        "business_name": "MSA Technologies",
        "owner_name": "MSA Admin",
        "phone": "03001234567",
        "email": "seller@msatechnologies.pk",
        "business_category": "Electronics",
        "business_address": "MSA Office, Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.both,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Tech House Quaidabad",
        "owner_name": "Ali Raza",
        "phone": "03011112222",
        "email": "techhouse@msa.local",
        "business_category": "Electronics",
        "business_address": "Main Bazaar, Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Home Comfort Store",
        "owner_name": "Sana Malik",
        "phone": "03022223333",
        "email": "homecomfort@msa.local",
        "business_category": "Home & Kitchen",
        "business_address": "Civil Line, Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.warehouse,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Urban Shoes",
        "owner_name": "Bilal Ahmed",
        "phone": "03033334444",
        "email": "urbanshoes@msa.local",
        "business_category": "Shoes",
        "business_address": "Shoe Market, Khushab",
        "city": "Khushab",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Style Market",
        "owner_name": "Ayesha Khan",
        "phone": "03044445555",
        "email": "stylemarket@msa.local",
        "business_category": "Fashion",
        "business_address": "Fashion Street, Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Khushab Fashion House",
        "owner_name": "Imran Shah",
        "phone": "03055556666",
        "email": "kfh@msa.local",
        "business_category": "Fashion",
        "business_address": "Khushab City",
        "city": "Khushab",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Beauty Point",
        "owner_name": "Nadia Bibi",
        "phone": "03066667777",
        "email": "beautypoint@msa.local",
        "business_category": "Beauty Products",
        "business_address": "Quaidabad Plaza",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.warehouse,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Quaidabad Mart",
        "owner_name": "Hassan Ali",
        "phone": "03077778888",
        "email": "qmart@msa.local",
        "business_category": "Groceries",
        "business_address": "Grain Market, Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Kitchen World",
        "owner_name": "Farah Noor",
        "phone": "03088889999",
        "email": "kitchenworld@msa.local",
        "business_category": "Home & Kitchen",
        "business_address": "Joharabad Road",
        "city": "Joharabad",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Baby Care Store",
        "owner_name": "Maryam Fatima",
        "phone": "03099990000",
        "email": "babycare@msa.local",
        "business_category": "Baby Products",
        "business_address": "Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Student Point",
        "owner_name": "Usman Tariq",
        "phone": "03101112222",
        "email": "studentpoint@msa.local",
        "business_category": "Books & Stationery",
        "business_address": "School Road, Quaidabad",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.own_shop,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
    {
        "business_name": "Daily Needs Store",
        "owner_name": "Kamran Iqbal",
        "phone": "03112223333",
        "email": "dailyneeds@msa.local",
        "business_category": "Daily Use Items",
        "business_address": "Quaidabad Bazaar",
        "city": "Quaidabad",
        "district": "Khushab",
        "selling_type": SellingType.both,
        "status": SellerStatus.approved,
        "is_verified": True,
        "password": "seller123",
    },
]

# name, category_slug, price, original, seller_name, badge, stock, image, features
PRODUCTS = [
    ("Wireless Bluetooth Earbuds", "mobile-accessories", 2499, 3499, "MSA Technologies", ProductBadge.msa_product, 45,
     "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=600&h=600&fit=crop",
     "Bluetooth 5.3\n24h playback\nTouch controls\nIPX5 water resistance"),
    ("Fast Charging USB-C Cable", "mobile-accessories", 699, 999, "MSA Technologies", ProductBadge.msa_product, 120,
     "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=600&h=600&fit=crop",
     "Fast charge up to 65W\nBraided nylon\n1.5 metre length"),
    ("Smart Watch Series X", "electronics", 6999, 8999, "Tech House Quaidabad", ProductBadge.verified_seller, 28,
     "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&h=600&fit=crop",
     "Heart rate monitoring\nMulti-sport modes\n7 days battery"),
    ("LED Desk Lamp", "home-kitchen", 1899, 2499, "Home Comfort Store", ProductBadge.warehouse_available, 8,
     "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=600&h=600&fit=crop",
     "3 brightness levels\nWarm & cool modes\nUSB-powered"),
    ("Men Casual Sneakers", "shoes", 4499, 5999, "Urban Shoes", ProductBadge.verified_seller, 34,
     "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=600&fit=crop",
     "Breathable mesh\nCushioned midsole\nAnti-slip outsole"),
    ("Women Handbag Premium", "fashion", 3999, 5499, "Style Market", ProductBadge.verified_seller, 19,
     "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600&h=600&fit=crop",
     "Premium finish\nMultiple compartments\nAdjustable strap"),
    ("Cotton Kurta Collection", "fashion", 2799, 3599, "Khushab Fashion House", ProductBadge.verified_seller, 52,
     "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=600&h=600&fit=crop",
     "100% soft cotton\nBreathable fit\nMachine washable"),
    ("Beauty Skin Care Kit", "beauty-products", 2299, 2999, "Beauty Point", ProductBadge.warehouse_available, 6,
     "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&h=600&fit=crop",
     "Daily cleanser\nHydrating moisturizer\nVitamin serum"),
    ("Perfume Classic Edition", "beauty-products", 1999, 2699, "MSA Technologies", ProductBadge.msa_product, 41,
     "https://images.unsplash.com/photo-1541643600914-78b084683601?w=600&h=600&fit=crop",
     "Long-lasting fragrance\n100ml bottle\nElegant packaging"),
    ("Grocery Value Pack", "groceries", 3499, 4199, "Quaidabad Mart", ProductBadge.verified_seller, 22,
     "https://images.unsplash.com/photo-1542838132-92d533900a3a?w=600&h=600&fit=crop",
     "Assorted pantry staples\nFamily-sized portions"),
    ("Cooking Oil 5L", "groceries", 2850, 3200, "Quaidabad Mart", ProductBadge.verified_seller, 75,
     "https://images.unsplash.com/photo-1474979266404-7ea320af5074?w=600&h=600&fit=crop",
     "5 litre pack\nPure refined quality"),
    ("Kitchen Blender", "home-kitchen", 5499, 6999, "Home Comfort Store", ProductBadge.warehouse_available, 15,
     "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=600&h=600&fit=crop",
     "High-speed motor\nStainless steel blades\nEasy-clean jar"),
    ("Non-Stick Cookware Set", "home-kitchen", 7999, 9999, "Kitchen World", ProductBadge.verified_seller, 11,
     "https://images.unsplash.com/photo-1556911220-bff31c987d48?w=600&h=600&fit=crop",
     "Non-stick coated\nHeat-resistant handles\nComplete set"),
    ("Baby Care Gift Pack", "baby-products", 2999, 3799, "Baby Care Store", ProductBadge.verified_seller, 18,
     "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=600&h=600&fit=crop",
     "Gentle lotion & wash\nSoft washcloths\nGift-ready"),
    ("Baby Feeding Bottle Set", "baby-products", 1199, 1599, "Baby Care Store", ProductBadge.verified_seller, 3,
     "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?w=600&h=600&fit=crop",
     "BPA-free\nAnti-colic design\nSteriliser safe"),
    ("School Stationery Bundle", "books-stationery", 899, 1299, "Student Point", ProductBadge.verified_seller, 90,
     "https://images.unsplash.com/photo-1452860606245-08befc0ff44b?w=600&h=600&fit=crop",
     "Pens & pencils\nErasers & notebooks"),
    ("Premium Notebook Pack", "books-stationery", 649, 899, "Student Point", ProductBadge.verified_seller, 140,
     "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=600&h=600&fit=crop",
     "Thick quality paper\nPack of 3\nDurable cover"),
    ("Cleaning Essentials Pack", "daily-use-items", 1499, 1899, "Daily Needs Store", ProductBadge.warehouse_available, 33,
     "https://images.unsplash.com/photo-1563453392212-326f5e854473?w=600&h=600&fit=crop",
     "Surface cleaners\nGloves & sponges"),
    ("Laundry Detergent Pack", "daily-use-items", 1299, 1599, "Daily Needs Store", ProductBadge.verified_seller, 0,
     "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?w=600&h=600&fit=crop",
     "Tough stain removal\nFresh scent\nFamily pack"),
    ("Power Bank 10000mAh", "electronics", 3299, 4299, "MSA Technologies", ProductBadge.msa_product, 37,
     "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=600&h=600&fit=crop",
     "10000mAh capacity\nDual USB output\nLED indicator"),
    ("Mobile Phone Stand", "mobile-accessories", 499, 799, "MSA Technologies", ProductBadge.msa_product, 200,
     "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=600&h=600&fit=crop",
     "Adjustable angles\nAnti-slip base\nFoldable"),
    ("Men Leather Wallet", "fashion", 1299, 1899, "Style Market", ProductBadge.verified_seller, 29,
     "https://images.unsplash.com/photo-1627123424574-724758594e93?w=600&h=600&fit=crop",
     "Multiple card slots\nSlim design\nGift packaging"),
    ("Home Storage Boxes", "home-kitchen", 2199, 2799, "Home Comfort Store", ProductBadge.warehouse_available, 5,
     "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=600&h=600&fit=crop",
     "Stackable design\nClear lids\nMulti-box set"),
    ("Kids Learning Book Set", "books-stationery", 1599, 2199, "Student Point", ProductBadge.verified_seller, 44,
     "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600&h=600&fit=crop",
     "Alphabet & numbers\nColourful illustrations\nAge-appropriate"),
]


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            print("Database already seeded. Skipping.")
            return

        # Admin
        admin = User(
            email="admin@msadigitalstore.pk",
            phone="03000000000",
            full_name="MSA Admin",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.admin,
        )
        db.add(admin)

        # Demo customer
        customer_user = User(
            email="customer@msa.local",
            phone="03009876543",
            full_name="Ahmed Khan",
            hashed_password=get_password_hash("customer123"),
            role=UserRole.customer,
        )
        db.add(customer_user)
        db.flush()
        db.add(
            Customer(
                user_id=customer_user.id,
                address="Street 4, Quaidabad",
                city="Quaidabad",
                district="Khushab",
            )
        )

        # Categories
        cat_map = {}
        for name, slug, desc, icon in CATEGORIES:
            cat = Category(name=name, slug=slug, description=desc, icon=icon)
            db.add(cat)
            db.flush()
            cat_map[slug] = cat

        # Sellers
        seller_map = {}
        for s in SELLERS:
            user = User(
                email=s["email"],
                phone=s["phone"],
                full_name=s["owner_name"],
                hashed_password=get_password_hash(s["password"]),
                role=UserRole.seller,
            )
            db.add(user)
            db.flush()
            seller = Seller(
                user_id=user.id,
                business_name=s["business_name"],
                owner_name=s["owner_name"],
                phone=s["phone"],
                email=s["email"],
                business_category=s["business_category"],
                business_address=s["business_address"],
                city=s["city"],
                district=s["district"],
                selling_type=s["selling_type"],
                status=s["status"],
                is_verified=s["is_verified"],
            )
            db.add(seller)
            db.flush()
            seller_map[s["business_name"]] = seller

        ratings = [4.6, 4.4, 4.7, 4.5, 4.3, 4.8, 4.5, 4.6, 4.4, 4.2, 4.5, 4.6, 4.7, 4.8, 4.5, 4.3, 4.4, 4.2, 4.5, 4.6, 4.1, 4.4, 4.3, 4.7]
        reviews = [128, 86, 214, 67, 95, 152, 110, 88, 73, 54, 201, 119, 167, 92, 64, 143, 58, 47, 176, 189, 41, 77, 53, 98]

        for i, (name, cat_slug, price, original, seller_name, badge, stock, image, features) in enumerate(PRODUCTS):
            wh = badge == ProductBadge.warehouse_available
            product = Product(
                name=name,
                slug=slugify(name),
                description=f"{name} — quality marketplace product available on MSA Digital Store. Trusted sellers, secure checkout, and local delivery from Quaidabad, District Khushab.",
                features=features,
                price=price,
                original_price=original,
                badge=badge,
                stock=stock,
                stock_status=compute_stock_status(stock),
                warehouse_available=wh,
                rating=ratings[i],
                review_count=reviews[i],
                delivery_info="Delivery within 2–4 working days across Khushab district.",
                return_policy="7-day easy return on unused sealed items.",
                category_id=cat_map[cat_slug].id,
                seller_id=seller_map[seller_name].id,
            )
            db.add(product)
            db.flush()
            db.add(ProductImage(product_id=product.id, url=image, is_primary=True, alt_text=name))
            db.add(
                Inventory(
                    product_id=product.id,
                    quantity=stock,
                    low_stock_threshold=10,
                    warehouse_location="MSA Warehouse Quaidabad" if wh else None,
                )
            )

        db.commit()
        print("Seed complete.")
        print("Admin: admin@msadigitalstore.pk / admin123")
        print("Customer: customer@msa.local / customer123")
        print("Seller: seller@msatechnologies.pk / seller123")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
