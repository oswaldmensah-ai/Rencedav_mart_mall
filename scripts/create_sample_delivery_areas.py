import os, sys, django

sys.path.append(r'c:\rencedav_mart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.orders.models import DeliveryArea

areas = [
    ('East Legon', '40.00'),
    ('Osu', '30.00'),
    ('Tema', '60.00'),
    ('Airport Residential', '55.00'),
]

for name, fee in areas:
    obj, created = DeliveryArea.objects.get_or_create(name=name, defaults={'delivery_fee': fee})
    if created:
        print('Created:', obj.name, obj.delivery_fee)
    else:
        print('Exists:', obj.name, obj.delivery_fee)
print('Done')
