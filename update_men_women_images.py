import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from store.models import Category

men_url = 'https://tse3.mm.bing.net/th/id/OIP.9GlKnIbl4MaOZ1cLkF6CAwHaLH?w=2160&h=3240&rs=1&pid=ImgDetMain&o=7&rm=3'

# Update Men category
men_cat = Category.objects.filter(name__icontains='men').first()
if men_cat:
    try:
        r = requests.get(men_url, timeout=15, allow_redirects=True)
        r.raise_for_status()
        content = ContentFile(r.content)
        filename = 'category_men.jpg'
        # delete old file
        try:
            men_cat.image.delete(save=False)
        except Exception:
            pass
        men_cat.image.save(filename, content, save=True)
        print(f"Updated Men category: {men_cat.name} -> {men_cat.image.url}")
    except Exception as e:
        print('Failed to download or save Men image:', e)
else:
    print("Men category not found")

# Remove Women category image
women_cat = Category.objects.filter(name__icontains='women').first()
if women_cat:
    try:
        women_cat.image.delete(save=False)
    except Exception:
        pass
    women_cat.image = ''
    women_cat.save()
    print(f"Removed image for Women category: {women_cat.name}")
else:
    print("Women category not found")
