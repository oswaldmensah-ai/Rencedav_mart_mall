from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product

def home(request):
    """
    Renders the main storefront home page.
    Fetches active categories and featured products for display.
    """
    categories = Category.objects.filter(is_active=True)
    # Fetch only active products, showing newest arrivals first
    products = Product.objects.filter(is_active=True)[:12]
    
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)

def product_detail(request, slug):
    """
    Renders an individual product's detailed description page.
    Allows users to see stock availability and choose quantities.
    """
    # Fetch product by unique SEO slug, ensuring it is active
    product = get_object_or_404(Product, slug=slug, is_active=True)
    quantity_options = range(1, min(product.stock_quantity, 10) + 1) if product.stock_quantity else range(0)

    context = {
        'product': product,
        'quantity_options': quantity_options,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    """
    Simple product search using the `q` GET parameter. Returns matching
    active products by name or description.
    """
    query = request.GET.get('q', '')
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(is_active=True).filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'store/search_results.html', context)


def category(request, slug):
    """
    List products for a given category slug.
    Reuses the `store/index.html` template but passes an `active_category`
    so the template can adjust headings if desired.
    """
    categories = Category.objects.filter(is_active=True)
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = category.products.filter(is_active=True)

    context = {
        'categories': categories,
        'products': products,
        'active_category': category,
    }
    return render(request, 'store/index.html', context)


def products_all(request):
    """Render a page listing all active products (no limit)."""
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/index.html', context)