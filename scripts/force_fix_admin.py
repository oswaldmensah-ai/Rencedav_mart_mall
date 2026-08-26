import os

from apps.accounts.models import User
from django.contrib.auth.hashers import check_password
email='florencedavor3@gmail.com'
u=User.objects.filter(email=email).first()
with open('admin_fix.txt','w', encoding='utf-8') as f:
    if not u:
        f.write('NOTFOUND')
    else:
        u.is_staff=True
        u.is_superuser=True
        u.is_admin=True
        u.is_active=True
        password = os.environ.get('ADMIN_PASSWORD')
        if not password:
            raise RuntimeError('Set ADMIN_PASSWORD before updating an administrator.')
        u.set_password(password)
        u.save()
        f.write(f'EMAIL:{u.email}\nIS_STAFF:{u.is_staff}\nIS_SUPERUSER:{u.is_superuser}\nIS_ADMIN:{u.is_admin}\nIS_ACTIVE:{u.is_active}\n')
        f.write('PW_OK:'+str(check_password(password, u.password))+'\n')
print('WROTE admin_fix.txt')
