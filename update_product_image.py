import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

import requests
from django.core.files.base import ContentFile
from store.models import Product

# Find the oversized white tee product
product = Product.objects.filter(name__icontains='oversized').first()

if product:
    url = 'https://sl.bing.net/jH8dzARzofQ'
    
    try:
        # Download the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Get image extension from URL or response headers
        content_type = response.headers.get('content-type', 'image/jpeg')
        if 'jpeg' in content_type or 'jpg' in content_type:
            ext = 'jpg'
        elif 'png' in content_type:
            ext = 'png'
        elif 'webp' in content_type:
            ext = 'webp'
        else:
            ext = 'jpg'
        
        # Create filename
        filename = f'oversized_white_tee_main.{ext}'
        
        # Save to image_main field
        product.image_main.save(
            filename,
            ContentFile(response.content),
            save=True
        )
        
        print(f"Successfully updated {product.name}")
        print(f"Image saved as: {filename}")
        print(f"New image path: {product.image_main.url}")
        
    except Exception as e:
        print(f"Error downloading image: {e}")
else:
    print("Oversized White Tee product not found")
