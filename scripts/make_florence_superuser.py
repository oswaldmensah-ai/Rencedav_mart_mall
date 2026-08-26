from django import setup
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
setup()
from apps.accounts.models import User
u = User.objects.filter(email='florencedavor3@gmail.com').first()
print('found', bool(u))
if u:
    u.is_staff = True
    u.is_superuser = True
    u.is_admin = True
    u.save()
    print('updated', u.email, u.is_staff, u.is_superuser, u.is_admin)
else:
    print('user not found')
