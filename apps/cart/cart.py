"""
Session-based Cart class.
The cart is stored entirely in the Django session as a dict:
  {
    "<product_id>": {
      "quantity": int,
      "price":    str   ← stored as string to avoid float serialisation issues
    }
  }
This class is instantiated on every request via the cart context processor.
"""

from decimal import Decimal
from django.conf import settings
from apps.store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _save(self):
        """Mark the session as modified so Django persists it."""
        self.session.modified = True

    # ── Public API ────────────────────────────────────────────────────────────

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self._save()

    def remove(self, product):
        """Remove a product from the cart entirely."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save()

    def clear(self):
        """Empty the cart (called after a successful order)."""
        del self.session[settings.CART_SESSION_ID]
        self._save()

    # ── Iteration & Aggregation ───────────────────────────────────────────────

    def __iter__(self):
        """
        Yields enriched cart item dicts for use in templates.
        Fetches products in a single query to avoid N+1.
        """
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)

        # Create a shallow copy of each inner item dict so we don't mutate
        # the session data when enriching items with product objects or
        # Decimal instances (those types are not JSON-serializable).
        cart_copy = {pid: item.copy() for pid, item in self.cart.items()}

        # Attach product objects to the copies
        for product in products:
            pid = str(product.id)
            if pid in cart_copy:
                cart_copy[pid]['product'] = product

        for item in cart_copy.values():
            item['price'] = Decimal(item['price'])
            item['line_total'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Total number of individual items (sum of quantities)."""
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return self.total_price

    @property
    def is_empty(self):
        return len(self.cart) == 0
