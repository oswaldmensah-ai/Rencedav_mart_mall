import json
import hmac
import hashlib
from decimal import Decimal
from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import constant_time_compare
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.orders.models import Order
from .models import Payment
from .paystack import verify_transaction


def build_payment_from_data(order, data):
    reference_value = data.get('reference')
    status = data.get('status', '').lower()
    amount = Decimal(data.get('amount') or 0) / Decimal(100)
    currency = data.get('currency', 'GHS')
    channel = data.get('channel', '')
    paid_at = data.get('paid_at')
    metadata = data.get('metadata', {}) or {}
    paystack_access_code = data.get('access_code', '') or ''

    payment, _ = Payment.objects.update_or_create(
        order=order,
        paystack_reference=reference_value,
        defaults={
            'amount': amount,
            'currency': currency,
            'status': status,
            'channel': channel,
            'metadata': metadata,
            'paid_at': paid_at if paid_at else None,
            'paystack_access_code': paystack_access_code,
        }
    )

    if status == 'success':
        order.status = 'Paid'
        order.save(update_fields=['status'])
    elif status in {'failed', 'abandoned'}:
        order.status = 'Pending'
        order.save(update_fields=['status'])

    return payment


def verify_webhook_signature(request):
    expected_secret = getattr(settings, 'PAYSTACK_WEBHOOK_SECRET', '')
    if not expected_secret:
        return False

    signature = request.headers.get('X-Paystack-Signature') or request.META.get('HTTP_X_PAYSTACK_SIGNATURE')
    if not signature:
        return False

    computed = hmac.new(expected_secret.encode('utf-8'), request.body, hashlib.sha512).hexdigest()
    return constant_time_compare(computed, signature)


def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'Pending':
        return redirect('orders:order_created')

    public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
    if not public_key:
        return render(request, 'payments/missing_keys.html', {'order': order})

    return render(request, 'payments/initiate.html', {
        'order': order,
        'paystack_public_key': public_key,
    })


def webhook_simulator(request):
    if request.method == 'POST':
        payload = request.POST.dict()
        order_id = payload.get('order_id')
        reference = payload.get('reference')
        status = payload.get('status', 'success')
        amount = payload.get('amount', '0')
        currency = payload.get('currency', 'GHS')
        metadata = {'order_id': order_id}

        if not order_id or not reference:
            raise Http404('order_id and reference are required')

        order = get_object_or_404(Order, id=order_id)
        data = {
            'reference': reference,
            'status': status,
            'amount': int(float(amount) * 100),
            'currency': currency,
            'metadata': metadata,
        }
        payment = build_payment_from_data(order, data)
        return render(request, 'payments/webhook_result.html', {'order': order, 'payment': payment})

    return render(request, 'payments/webhook_simulator.html')


@require_POST
def payment_callback(request):
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    reference_value = payload.get('reference')
    order_id = payload.get('order_id')
    if not order_id or not reference_value:
        return JsonResponse({'error': 'Missing order_id or reference'}, status=400)

    try:
        verified = verify_transaction(reference_value)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=400)

    data = verified.get('data', {})
    metadata = data.get('metadata', {}) or {}
    metadata_order_id = metadata.get('order_id')
    if str(metadata_order_id) != str(order_id):
        return JsonResponse({'error': 'Order ID mismatch on Paystack metadata'}, status=400)

    order = get_object_or_404(Order, id=order_id)
    payment = build_payment_from_data(order, data)

    return JsonResponse({'status': 'ok', 'payment_id': payment.id})


@csrf_exempt
@require_POST
def payment_webhook(request):
    if not verify_webhook_signature(request):
        return JsonResponse({'error': 'Invalid webhook signature'}, status=400)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    event = payload.get('event')
    data = payload.get('data', {})
    if event not in {'charge.success', 'charge.failed', 'payment.expired', 'charge.dispute'}:
        return JsonResponse({'status': 'ignored'})

    metadata = data.get('metadata', {}) or {}
    order_id = metadata.get('order_id')
    reference_value = data.get('reference')

    if not order_id or not reference_value:
        return JsonResponse({'error': 'Missing order_id or reference'}, status=400)

    order = get_object_or_404(Order, id=order_id)
    payment = build_payment_from_data(order, data)

    return JsonResponse({'status': 'ok', 'payment_id': payment.id})
