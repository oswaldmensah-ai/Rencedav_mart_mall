"""
Injects the cart object into every template so the nav cart-count badge
stays in sync without extra view logic.
"""

from .cart import Cart


def cart_context(request):
    return {'cart': Cart(request)}
