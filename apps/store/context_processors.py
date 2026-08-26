"""
Injects site-wide context into every template:
  - SITE_NAME
  - SITE_URL
  - categories (for navbar and global access)
"""

from django.conf import settings
from .models import Category
from apps.orders.models import Order


def site_context(request):
    # Fetch all active categories for navbar menus
    categories = Category.objects.filter(is_active=True)
    new_order_count = 0
    if request.user.is_authenticated and request.user.is_admin:
      new_order_count = Order.objects.filter(needs_review=True).count()
    
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL':  settings.SITE_URL,
        'categories': categories,
        'new_order_count': new_order_count,
    }
