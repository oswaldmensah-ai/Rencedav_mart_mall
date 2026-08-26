from django.contrib import messages
from django.shortcuts import redirect, render

from apps.orders.models import Order

from .decorators import admin_required
from .forms import CategoryForm, ProductForm


@admin_required
def overview(request):
    orders = Order.objects.prefetch_related('items__product').all()[:10]
    return render(request, 'dashboard/overview.html', {
        'orders': orders,
        'category_form': CategoryForm(),
        'product_form': ProductForm(),
    })


@admin_required
def add_category(request):
    if request.method != 'POST':
        return redirect('dashboard:overview')

    form = CategoryForm(request.POST, request.FILES)
    if form.is_valid():
        category = form.save()
        messages.success(request, f'{category.name} was added to the catalogue.')
        return redirect('dashboard:overview')

    orders = Order.objects.prefetch_related('items__product').all()[:10]
    return render(request, 'dashboard/overview.html', {
        'orders': orders,
        'category_form': form,
        'product_form': ProductForm(),
    })


@admin_required
def add_product(request):
    if request.method != 'POST':
        return redirect('dashboard:overview')

    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save()
        messages.success(request, f'{product.name} was added to the catalogue.')
        return redirect('dashboard:overview')

    orders = Order.objects.prefetch_related('items__product').all()[:10]
    return render(request, 'dashboard/overview.html', {
        'orders': orders,
        'category_form': CategoryForm(),
        'product_form': form,
    })


@admin_required
def review_order(request, order_id):
    if request.method == 'POST':
        Order.objects.filter(id=order_id, needs_review=True).update(needs_review=False)
        messages.success(request, f'Order #{order_id} marked as reviewed.')
    return redirect('dashboard:overview')
