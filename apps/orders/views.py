from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from apps.cart.cart import Cart
from django.core.mail import mail_admins, send_mail
from django.conf import settings





def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('store:home')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            # Calculate total based on fulfillment type
            fulfillment_type = form.cleaned_data['fulfillment_type']
            order.total_amount = cart.get_total_price()
            
            if fulfillment_type == 'delivery':
                # User provides a full delivery address (including landmark)
                order.delivery_area = None
                order.delivery_address = form.cleaned_data.get('delivery_address', '')
                order.delivery_special_message = form.cleaned_data.get('delivery_special_message', '')
            else:
                order.delivery_area = None
                order.delivery_address = ''
                order.delivery_special_message = ''

            order.save()


            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                product = item['product']
                product.stock_quantity -= item['quantity']
                product.save()

            try:
                subject = f'New order #{order.id} placed'
                lines = [
                    f'Order ID: {order.id}',
                    f'Customer: {order.full_name or "(guest)"}',
                    f'Phone: {order.phone_number}',
                    f'Email: {order.email or "(not provided)"}',
                    f'Fulfillment: {order.get_fulfillment_type_display()}',
                ]
                
                if order.fulfillment_type == 'delivery':
                    lines.extend([
                        f'Address: {order.delivery_address}',
                        f'Special message: {order.delivery_special_message}',
                    ])

                
                lines.extend([
                    f'Total: GH₵ {order.total_amount}',
                    'Items:'
                ])
                
                for item in order.items.all():
                    lines.append(f'- {item.product.name} x{item.quantity} @ GH₵ {item.price}')
                body = '\n'.join(lines)

                if getattr(settings, 'ADMINS', None):
                    mail_admins(subject, body)
                else:
                    to_addr = getattr(settings, 'EMAIL_HOST_USER', None) or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                    from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or to_addr
                    if to_addr and from_addr:
                        send_mail(subject, body, from_addr, [to_addr])
            except Exception:
                pass

            request.session['order_id'] = order.id
            cart.clear()
            return redirect('payments:initiate_payment', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
    })


def order_created(request):
    """Simple confirmation page right after clicking checkout."""
    order_id = request.session.get('order_id')
    order = None
    subtotal = None
    if order_id:
        try:
            order = Order.objects.prefetch_related('items__product').get(id=order_id)
            subtotal = sum([item.get_cost() for item in order.items.all()])
        except Order.DoesNotExist:
            order = None

    return render(request, 'orders/created.html', {'order_id': order_id, 'order': order, 'subtotal': subtotal})