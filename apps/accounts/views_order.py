from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from apps.orders.models import Order


@login_required
def order_history(request):
    qs = request.user.order_set.prefetch_related('items__product').order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 10)
    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)

    context = {
        'orders': orders_page,
        'page_obj': orders_page,
        'is_paginated': orders_page.has_other_pages(),
    }
    return render(request, 'accounts/order_history.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(request.user.order_set.prefetch_related('items__product'), id=order_id)
    subtotal = sum(item.get_cost() for item in order.items.all())
    return render(request, 'accounts/order_detail.html', {'order': order, 'subtotal': subtotal})
