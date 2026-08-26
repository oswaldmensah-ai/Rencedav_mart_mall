import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
import django
django.setup()
from django.conf import settings
from django.core.mail import send_mail

recipient = 'florencedavor3@gmail.com'
from_addr = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or getattr(settings, 'EMAIL_HOST_USER', None) or 'no-reply@localhost'
subject = 'Test: Order notification from Rencedav Mart'
body = 'This is a test order notification from the Rencedav Mart app.'

try:
    count = send_mail(subject, body, from_addr, [recipient])
    print('send_mail returned', count)
except Exception as e:
    print('send failed:', type(e).__name__, str(e))
