"""Sample data so the shop is not empty on first start."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models

CATALOG = {
    "Electronics": ["Laptops", "Phones", "Headphones"],
    "Clothing": ["T-Shirts", "Shoes"],
    "Home": ["Kitchen", "Furniture"],
}

BRANDS = ["Apple", "Samsung", "Sony", "Lenovo", "Nike", "Adidas", "Philips", "IKEA"]

# (name, category, subcategory, brand, price, short description, details)
PRODUCTS = [
    ("MacBook Air 13 M3", "Electronics", "Laptops", "Apple", 3499.0,
     "Thin and light laptop with all-day battery.",
     "13.6-inch display, 8-core CPU, 16 GB RAM, 256 GB SSD, up to 18 hours of battery."),
    ("ThinkPad X1 Carbon", "Electronics", "Laptops", "Lenovo", 4199.0,
     "Business laptop with a great keyboard.",
     "14-inch display, Intel Core Ultra 7, 32 GB RAM, 1 TB SSD, 1.1 kg."),
    ("IdeaPad Slim 5", "Electronics", "Laptops", "Lenovo", 1899.0,
     "Everyday laptop at a fair price.",
     "15.3-inch display, AMD Ryzen 7, 16 GB RAM, 512 GB SSD."),
    ("iPhone 16", "Electronics", "Phones", "Apple", 2999.0,
     "Apple smartphone with a 48 MP camera.",
     "6.1-inch OLED display, A18 chip, 128 GB storage, USB-C."),
    ("Galaxy S25", "Electronics", "Phones", "Samsung", 2799.0,
     "Samsung flagship phone.",
     "6.2-inch AMOLED 120 Hz, 12 GB RAM, 256 GB storage, triple camera."),
    ("Galaxy A56", "Electronics", "Phones", "Samsung", 1199.0,
     "Mid-range phone with a big battery.",
     "6.7-inch display, 8 GB RAM, 128 GB storage, 5000 mAh battery."),
    ("WH-1000XM5", "Electronics", "Headphones", "Sony", 1049.0,
     "Wireless noise-cancelling headphones.",
     "Over-ear, 30 hours of battery, multipoint Bluetooth, quick charge."),
    ("AirPods Pro 2", "Electronics", "Headphones", "Apple", 749.0,
     "In-ear earbuds with active noise cancellation.",
     "USB-C case, adaptive audio, up to 6 hours per charge."),
    ("Galaxy Buds3", "Electronics", "Headphones", "Samsung", 499.0,
     "Compact wireless earbuds.",
     "Open-type design, 24-bit sound, IP57 water resistance."),
    ("Dri-FIT Running Tee", "Clothing", "T-Shirts", "Nike", 89.0,
     "Lightweight sports T-shirt.",
     "Sweat-wicking fabric, regular fit, 100% recycled polyester."),
    ("Essentials Logo Tee", "Clothing", "T-Shirts", "Adidas", 69.0,
     "Classic cotton T-shirt.",
     "Soft cotton jersey, crew neck, regular fit."),
    ("Air Zoom Pegasus 41", "Clothing", "Shoes", "Nike", 399.0,
     "Everyday running shoes.",
     "Responsive foam, breathable mesh upper, rubber outsole."),
    ("Ultraboost 5", "Clothing", "Shoes", "Adidas", 479.0,
     "Comfortable running shoes.",
     "Boost midsole, Primeknit upper, Continental rubber outsole."),
    ("Airfryer XL", "Home", "Kitchen", "Philips", 449.0,
     "Fry, bake and grill with little or no oil.",
     "6.2 L basket, 2000 W, 7 presets, dishwasher-safe parts."),
    ("Electric Kettle 1.7 L", "Home", "Kitchen", "Philips", 119.0,
     "Fast-boiling stainless steel kettle.",
     "1.7 L, 2200 W, auto shut-off, limescale filter."),
    ("POÄNG Armchair", "Home", "Furniture", "IKEA", 399.0,
     "Comfortable bentwood armchair.",
     "Birch veneer frame, washable cushion cover, 68 x 82 x 100 cm."),
    ("KALLAX Shelf", "Home", "Furniture", "IKEA", 249.0,
     "Shelving unit that works as a room divider.",
     "4 x 4 compartments, 147 x 147 cm, white finish."),
]

# (product name, first name, last name, stars, text)
REVIEWS = [
    ("MacBook Air 13 M3", "Nino", "Beridze", 5, "Very fast and silent, battery lasts all day."),
    ("MacBook Air 13 M3", "Giorgi", "Kapanadze", 4, "Great laptop, only 256 GB is a bit small."),
    ("ThinkPad X1 Carbon", "Luka", "Maisuradze", 5, "Best keyboard I have used."),
    ("iPhone 16", "Mariam", "Gelashvili", 4, "Good camera, the price is high."),
    ("Galaxy S25", "Dato", "Lomidze", 5, "Beautiful screen and very smooth."),
    ("Galaxy A56", "Ana", "Tsiklauri", 3, "Fine for the price, the camera is average."),
    ("WH-1000XM5", "Sandro", "Chkheidze", 5, "Noise cancelling is amazing on flights."),
    ("WH-1000XM5", "Tamar", "Abashidze", 4, "Very comfortable, the case is big."),
    ("Air Zoom Pegasus 41", "Irakli", "Janelidze", 5, "Perfect for daily running."),
    ("Airfryer XL", "Salome", "Kvaratskhelia", 4, "Easy to clean and cooks evenly."),
    ("KALLAX Shelf", "Levan", "Gogoladze", 3, "Good shelf, assembly takes time."),
]


def seed_if_empty(db: Session) -> None:
    if db.scalar(select(models.Product.id).limit(1)) is not None:
        return

    categories, subcategories = {}, {}
    for cat_name, subs in CATALOG.items():
        cat = models.Category(name=cat_name)
        db.add(cat)
        categories[cat_name] = cat
        for sub_name in subs:
            sub = models.Subcategory(name=sub_name, category=cat)
            db.add(sub)
            subcategories[sub_name] = sub

    brands = {name: models.Brand(name=name) for name in BRANDS}
    db.add_all(brands.values())

    products = {}
    for i, (name, cat, sub, brand, price, short, details) in enumerate(PRODUCTS, start=1):
        p = models.Product(
            name=name,
            category=categories[cat],
            subcategory=subcategories[sub],
            brand=brands[brand],
            price=price,
            short_description=short,
            details=details,
            image_url=f"https://picsum.photos/seed/eshop{i}/400/400",
            stock=50,
        )
        db.add(p)
        products[name] = p

    for product_name, first, last, stars, text in REVIEWS:
        db.add(models.Review(product=products[product_name], first_name=first,
                             last_name=last, rating=stars, text=text))
    db.commit()
