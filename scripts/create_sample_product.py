import os, sys, django
from django.core.files import File

sys.path.append(r'c:\rencedav_mart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.store.models import Category, Product

category, _ = Category.objects.get_or_create(name='Sample Category', defaults={'slug': 'sample-category'})
product, created = Product.objects.get_or_create(
    name='Sample Product',
    defaults={
        'category': category,
        'description': 'Sample product created for direct image upload testing.',
        'price': '9.99',
        'stock_quantity': 10,
        'is_featured': True,
        'is_active': True,
    }
)

# Use the local static placeholder so the dev server shows an image immediately
sample_local = '/static/img/product-placeholder.svg'
product.image_url = sample_local
product.save()
print('PRODUCT', product.pk, product.name, 'IMAGE_URL', product.image_url)
