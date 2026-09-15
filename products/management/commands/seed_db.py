from django.core.management.base import BaseCommand
from categories.models import Category
from products.models import Product

class Command(BaseCommand):
    help = "Seeds the database with categories and products for testing."

    def handle(self, *args, **options):
        # 1. Seed Categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest gadgets, smartphones, laptops and accessories',
                'image': 'categories/electronics.png',
                'is_active': True,
            },
            {
                'name': 'Fashion',
                'description': 'Trendy apparel, footwear, and accessories for men and women',
                'image': 'categories/fashion.png',
                'is_active': True,
            },
            {
                'name': 'Home & Kitchen',
                'description': 'Premium home decor, kitchen appliances, and daily essentials',
                'image': 'categories/home_kitchen.png',
                'is_active': True,
            },
            {
                'name': 'Books',
                'description': 'Best-selling novels, educational books, and stationery',
                'image': 'categories/books.png',
                'is_active': True,
            },
            {
                'name': 'Beverages',
                'description': 'Refreshing drinks, coffee, tea, and juices',
                'image': 'categories/beverages.png',
                'is_active': True,
            },
        ]

        self.stdout.write("--- Seeding Categories ---")
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_data['name'])
            cat.description = cat_data['description']
            cat.image = cat_data['image']
            cat.is_active = cat_data['is_active']
            cat.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category '{cat.name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated category '{cat.name}'"))

        # 2. Seed Products
        products_data = [
            # Electronics
            {
                'category_name': 'Electronics',
                'name': 'Wireless Noise-Canceling Headphones',
                'description': 'Premium over-ear wireless headphones with advanced active noise cancellation, 40-hour battery life, and crystal-clear audio quality.',
                'price': 199.99,
                'discount_price': 179.99,
                'stock': 50,
                'image': 'products/headphones.png',
                'sku': 'ELEC-HEAD-001',
                'is_available': True,
            },
            {
                'category_name': 'Electronics',
                'name': 'Smart Fitness Watch',
                'description': 'Track your fitness, heart rate, sleep patterns, and daily steps with this sleek, waterproof smartwatch. 7-day battery life and built-in GPS.',
                'price': 89.99,
                'discount_price': 79.99,
                'stock': 120,
                'image': 'products/smartwatch.png',
                'sku': 'ELEC-WATCH-002',
                'is_available': True,
            },
            {
                'category_name': 'Electronics',
                'name': 'Portable Bluetooth Speaker',
                'description': 'Compact and waterproof wireless speaker with booming 360-degree sound. Ideal for outdoor gatherings, travel, and home enjoyment.',
                'price': 59.99,
                'discount_price': None,
                'stock': 80,
                'image': 'products/speaker.png',
                'sku': 'ELEC-SPK-003',
                'is_available': True,
            },
            {
                'category_name': 'Electronics',
                'name': 'Mechanical Gaming Keyboard',
                'description': 'Tactile mechanical blue switches, customizable RGB backlighting, and anti-ghosting keys for the ultimate typing and gaming experience.',
                'price': 129.99,
                'discount_price': 109.99,
                'stock': 35,
                'image': 'products/keyboard.png',
                'sku': 'ELEC-KYBD-004',
                'is_available': True,
            },
            # Fashion
            {
                'category_name': 'Fashion',
                'name': 'Classic Denim Jacket',
                'description': 'Timeless blue denim jacket crafted from 100% organic premium cotton. Relaxed fit with metal button closures and front flap pockets.',
                'price': 69.99,
                'discount_price': 54.99,
                'stock': 40,
                'image': 'products/denim_jacket.png',
                'sku': 'FASH-JKT-001',
                'is_available': True,
            },
            {
                'category_name': 'Fashion',
                'name': 'Minimalist Leather Backpack',
                'description': 'Sleek, handcrafted top-grain leather backpack. Features a padded laptop sleeve, hidden anti-theft pockets, and adjustable shoulder straps.',
                'price': 85.00,
                'discount_price': None,
                'stock': 25,
                'image': 'products/backpack.png',
                'sku': 'FASH-BAG-002',
                'is_available': True,
            },
            {
                'category_name': 'Fashion',
                'name': 'Athletic Running Sneakers',
                'description': 'High-performance running sneakers featuring a breathable mesh upper, responsive cushioned midsole, and durable rubber traction outsole.',
                'price': 110.00,
                'discount_price': 95.00,
                'stock': 60,
                'image': 'products/sneakers.png',
                'sku': 'FASH-SHOE-003',
                'is_available': True,
            },
            {
                'category_name': 'Fashion',
                'name': 'Premium Cotton Hoodie',
                'description': 'Ultra-soft fleece hoodie made from organic cotton blend. Features a cozy drawstring hood and a spacious kangaroo front pocket.',
                'price': 49.99,
                'discount_price': None,
                'stock': 100,
                'image': 'products/hoodie.png',
                'sku': 'FASH-HD-004',
                'is_available': True,
            },
            # Home & Kitchen
            {
                'category_name': 'Home & Kitchen',
                'name': 'Double-Walled Coffee Mug',
                'description': 'Set of 2 insulated double-wall borosilicate glass coffee cups. Keeps your coffee hot and hands cool. Dishwasher and microwave safe.',
                'price': 18.50,
                'discount_price': None,
                'stock': 150,
                'image': 'products/coffee_mug.png',
                'sku': 'HOME-MUG-001',
                'is_available': True,
            },
            {
                'category_name': 'Home & Kitchen',
                'name': 'Stainless Steel Water Bottle',
                'description': 'Double-wall vacuum-insulated water bottle made from food-grade stainless steel. Keeps beverages cold for 24 hours or hot for 12 hours.',
                'price': 24.99,
                'discount_price': None,
                'stock': 200,
                'image': 'products/water_bottle.png',
                'sku': 'HOME-BTL-002',
                'is_available': True,
            },
            {
                'category_name': 'Home & Kitchen',
                'name': 'Electric Gooseneck Kettle',
                'description': 'Matte black electric kettle with precision-pour gooseneck spout, rapid-boil technology, and auto shut-off safety protection.',
                'price': 75.00,
                'discount_price': 65.00,
                'stock': 30,
                'image': 'products/kettle.png',
                'sku': 'HOME-KET-003',
                'is_available': True,
            },
            {
                'category_name': 'Home & Kitchen',
                'name': 'Scented Soy Candle Set',
                'description': 'Three premium aromatherapy soy candles infused with natural lavender, eucalyptus, and vanilla essential oils. 30-hour burn time each.',
                'price': 29.99,
                'discount_price': None,
                'stock': 75,
                'image': 'products/candles.png',
                'sku': 'HOME-CDL-004',
                'is_available': True,
            },
            # Books
            {
                'category_name': 'Books',
                'name': 'Dune (Deluxe Edition)',
                'description': 'Hardcover collector\'s edition of Frank Herbert\'s science fiction masterpiece. Features gorgeous endpapers, custom illustrations, and detailed maps.',
                'price': 30.00,
                'discount_price': None,
                'stock': 15,
                'image': 'products/dune.png',
                'sku': 'BOOK-DUNE-001',
                'is_available': True,
            },
            {
                'category_name': 'Books',
                'name': 'Atomic Habits',
                'description': 'James Clear\'s bestselling guide to building good habits, breaking bad ones, and making tiny daily changes that lead to remarkable results.',
                'price': 21.99,
                'discount_price': 17.99,
                'stock': 110,
                'image': 'products/atomic_habits.png',
                'sku': 'BOOK-HABIT-002',
                'is_available': True,
            },
            {
                'category_name': 'Books',
                'name': 'Classic Hardcover Journal',
                'description': 'Premium lined writing journal with 200 pages of thick ink-proof paper. Hardcover binding, elastic band closure, and expandible inner folder pocket.',
                'price': 15.00,
                'discount_price': None,
                'stock': 250,
                'image': 'products/journal.png',
                'sku': 'BOOK-JRNL-003',
                'is_available': True,
            },
            # Beverages
            {
                'category_name': 'Beverages',
                'name': 'Organic Matcha Green Tea',
                'description': 'Ceremonial grade pure Japanese matcha tea powder. Stone-ground, rich in antioxidants, naturally sweet, and vibrant green color.',
                'price': 28.00,
                'discount_price': 24.99,
                'stock': 45,
                'image': 'products/matcha.png',
                'sku': 'BEV-MTC-001',
                'is_available': True,
            },
            {
                'category_name': 'Beverages',
                'name': 'Single-Origin Coffee Beans',
                'description': 'Artisanal whole bean coffee sourced from Ethiopian highlands. Medium roast with complex floral notes, bright acidity, and sweet finish.',
                'price': 19.50,
                'discount_price': None,
                'stock': 90,
                'image': 'products/coffee_beans.png',
                'sku': 'BEV-CF-002',
                'is_available': True,
            },
            {
                'category_name': 'Beverages',
                'name': 'Sparkling Herbal Water',
                'description': 'Zero calorie refreshing carbonated mineral water infused with organic lemon, mint, and hibiscus extracts. Pack of 12 cans.',
                'price': 3.50,
                'discount_price': None,
                'stock': 500,
                'image': 'products/sparkling_water.png',
                'sku': 'BEV-WAT-003',
                'is_available': True,
            },
        ]

        self.stdout.write("\n--- Seeding Products ---")
        for prod_data in products_data:
            cat = Category.objects.get(name=prod_data['category_name'])
            prod = Product.objects.filter(sku=prod_data['sku']).first()
            if not prod:
                prod = Product(sku=prod_data['sku'], category=cat)
                created = True
            else:
                created = False
            
            prod.category = cat
            prod.name = prod_data['name']
            prod.description = prod_data['description']
            prod.price = prod_data['price']
            prod.discount_price = prod_data['discount_price']
            prod.stock = prod_data['stock']
            prod.image = prod_data['image']
            prod.is_available = prod_data['is_available']
            prod.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product '{prod.name}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Updated product '{prod.name}'"))

        self.stdout.write(self.style.SUCCESS("\nDatabase seeding completed successfully!"))
