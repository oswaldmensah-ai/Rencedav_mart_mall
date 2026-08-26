import os

from apps.accounts.models import User
from django.contrib.auth.hashers import check_password
email = 'florencedavor3@gmail.com'
u = User.objects.filter(email=email).first()
if not u:
    print('NOTFOUND')
else:
    print('EMAIL', u.email)
    print('IS_STAFF', u.is_staff)
    print('IS_SUPERUSER', u.is_superuser)
    print('IS_ADMIN', u.is_admin)
    password = os.environ.get('ADMIN_PASSWORD')
    print('PW_OK', check_password(password, u.password) if password else 'SKIPPED (ADMIN_PASSWORD not set)')
    print('PW_HASH_SNIPPET', u.password[:60])
