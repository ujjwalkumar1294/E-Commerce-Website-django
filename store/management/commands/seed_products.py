from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFont
import io
import random

from store.models import Category, Product


class Command(BaseCommand):
    help = 'Seed database with sample categories and products with generated images'

    def generate_product_image(self, product_name, bg_color, text_color='white'):
        """Generate a realistic-looking product image using PIL"""
        img = Image.new('RGB', (500, 600), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add product name text
        text = product_name[:20]
        text_width = draw.textlength(text)
        x = (500 - text_width) // 2
        y = 280
        
        try:
            # Try to use a larger font
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        draw.text((x, y), text, fill=text_color, font=font)
        
        # Save to bytes
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=85)
        img_io.seek(0)
        return img_io.read()

    def handle(self, *args, **options):
        categories = [
            {'name': 'Men', 'description': 'Premium menswear collection featuring contemporary styles'},
            {'name': 'Women', 'description': 'Curated womenswear with trendy and timeless pieces'},
            {'name': 'Accessories', 'description': 'Complete your look with our exclusive accessories range'},
        ]

        created_categories = {}
        for c in categories:
            obj, created = Category.objects.get_or_create(name=c['name'], defaults={'description': c['description']})
            created_categories[c['name']] = obj
            action = 'Created' if created else 'Found'
            self.stdout.write(f"{action} category: {obj.name}")

        sample_products = [
            # Men's Collection
            {'name': 'Oversized White Tee', 'price': 799.00, 'category': 'Men', 'desc': 'Classic oversized cotton tee in crisp white. Perfect for everyday wear.'},
            {'name': 'Black Slim Fit Jeans', 'price': 2299.00, 'category': 'Men', 'desc': 'Premium black denim with a sleek slim fit. Versatile and timeless.'},
            {'name': 'Charcoal Wool Blazer', 'price': 6999.00, 'category': 'Men', 'desc': 'Tailored wool blazer in charcoal grey. Elevate any outfit.'},
            {'name': 'Navy Linen Shirt', 'price': 1899.00, 'category': 'Men', 'desc': 'Lightweight linen shirt in navy. Ideal for warm weather style.'},
            {'name': 'Beige Chinos', 'price': 1699.00, 'category': 'Men', 'desc': 'Comfortable chinos in neutral beige. Pairs with anything.'},
            
            # Women's Collection
            {'name': 'Silk White Shirt Dress', 'price': 4299.00, 'category': 'Women', 'desc': 'Elegant silk shirt dress in white. Effortlessly chic.'},
            {'name': 'Black Pleated Midi Skirt', 'price': 2599.00, 'category': 'Women', 'desc': 'Sophisticated pleated midi skirt in black. Timeless elegance.'},
            {'name': 'Cream Knit Sweater', 'price': 2199.00, 'category': 'Women', 'desc': 'Cozy ribbed knit sweater in cream. Perfect for layering.'},
            {'name': 'Denim Jacket Blue', 'price': 3299.00, 'category': 'Women', 'desc': 'Classic denim jacket in faded blue. A wardrobe essential.'},
            {'name': 'Olive Green Pants', 'price': 2099.00, 'category': 'Women', 'desc': 'Tailored trousers in olive green. Modern and versatile.'},
            
            # Accessories Collection
            {'name': 'Leather Crossbody Bag', 'price': 3999.00, 'category': 'Accessories', 'desc': 'Genuine leather crossbody bag in cognac. Functional and stylish.'},
            {'name': 'Black Canvas Tote', 'price': 1599.00, 'category': 'Accessories', 'desc': 'Spacious canvas tote in black. Perfect for daily errands.'},
            {'name': 'Merino Wool Scarf', 'price': 1299.00, 'category': 'Accessories', 'desc': 'Soft merino wool scarf in grey. Cozy and luxurious.'},
            {'name': 'Minimalist Watch', 'price': 4999.00, 'category': 'Accessories', 'desc': 'Sleek minimalist watch with leather strap. Timeless design.'},
            {'name': 'Wide Brim Hat', 'price': 1899.00, 'category': 'Accessories', 'desc': 'Elegant wide-brim hat in cream. Sun protection with style.'},
        ]

        # Color palette for different products
        colors = [
            (240, 240, 240),  # Light grey
            (220, 220, 220),  # Medium grey
            (200, 200, 200),  # Darker grey
            (180, 180, 180),  # Even darker
            (160, 160, 160),  # Charcoal
            (100, 120, 140),  # Blue grey
            (140, 100, 120),  # Rose grey
            (120, 140, 100),  # Green grey
            (140, 130, 110),  # Brown grey
            (130, 130, 140),  # Purple grey
            (150, 140, 130),  # Warm grey
            (130, 140, 150),  # Cool grey
            (120, 110, 130),  # Purple
            (140, 120, 100),  # Tan
            (100, 130, 120),  # Teal
        ]
        
        for idx, p in enumerate(sample_products):
            cat = created_categories.get(p['category'])
            slug = slugify(p['name'])
            prod, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'price': p['price'],
                    'description': p['desc'],
                    'stock': 15,
                    'is_new': True,
                    'category': cat,
                }
            )
            if created:
                color_main = colors[idx % len(colors)]
                color_hover = colors[(idx + 1) % len(colors)]
                
                img_main = self.generate_product_image(p['name'], color_main)
                img_hover = self.generate_product_image(p['name'], color_hover)
                
                prod.image_main.save(f"{slug}-main.jpg", ContentFile(img_main), save=False)
                prod.image_hover.save(f"{slug}-hover.jpg", ContentFile(img_hover), save=False)
                prod.save()
                self.stdout.write(self.style.SUCCESS(f"✓ Created: {prod.name} - Rs. {prod.price}"))
            else:
                self.stdout.write(f"Already exists: {prod.name}")

        self.stdout.write(self.style.SUCCESS('\n✨ Seeding complete! 15 fashion products with generated images ready to shop.'))
