from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from apps.store.models import Product
from .cart import Cart
from django.http import JsonResponse
from django.template.loader import render_to_string

@require_POST
def cart_add(request, product_id):
    """Adds an item to the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    # Updated to match Claude's 'stock_quantity' field name
    if quantity <= product.stock_quantity:
        cart.add(product=product, quantity=quantity)
        
    # If this is an AJAX request, return JSON so the frontend can update
    # the cart indicator without a full page redirect.
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        mini_html = render_to_string('cart/mini_cart.html', {'cart': cart}, request=request)
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'mini_cart_html': mini_html,
        })

    # Stay on the same page after adding to cart. Prefer the HTTP Referer
    # so the user remains on the product or listing they were viewing.
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('store:home')

def cart_remove(request, product_id):
    """Removes an item from the cart."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    # If AJAX, return updated mini-cart HTML so frontend can refresh the popover
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        mini_html = render_to_string('cart/mini_cart.html', {'cart': cart}, request=request)
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'mini_cart_html': mini_html,
        })
    return redirect('cart:detail')

def cart_detail(request):
    """Renders the shopping cart page."""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})