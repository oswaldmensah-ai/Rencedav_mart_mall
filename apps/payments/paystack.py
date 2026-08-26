import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

PAYSTACK_BASE_URL = 'https://api.paystack.co'
VERIFY_ENDPOINT = PAYSTACK_BASE_URL + '/transaction/verify/{reference}'


def get_headers():
    secret = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
    if not secret:
        raise ImproperlyConfigured('PAYSTACK_SECRET_KEY must be set in settings or environment')
    return {
        'Authorization': f'Bearer {secret}',
        'Content-Type': 'application/json',
    }


def verify_transaction(reference: str) -> dict:
    if not reference:
        raise ValueError('Missing Paystack transaction reference')

    headers = get_headers()
    response = requests.get(VERIFY_ENDPOINT.format(reference=reference), headers=headers, timeout=15)
    response.raise_for_status()
    payload = response.json()
    if not payload.get('status'):
        raise ValueError('Paystack verification returned unsuccessful status')
    return payload
