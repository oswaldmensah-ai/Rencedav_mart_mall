from apps.accounts.models import User
from django.contrib.auth.hashers import check_password
email='florencedavor3@gmail.com'
u=User.objects.filter(email=email).first()
with open('admin_verify.txt','w', encoding='utf-8') as f:
    if not u:
        f.write('NOTFOUND')
    else:
        f.write(f'EMAIL:{u.email}\n')
        f.write(f'IS_STAFF:{u.is_staff}\n')
        f.write(f'IS_SUPERUSER:{u.is_superuser}\n')
        f.write(f'IS_ADMIN:{u.is_admin}\n')
        f.write(f'IS_ACTIVE:{u.is_active}\n')
            password = os.environ.get('ADMIN_PASSWORD')
            f.write(f'PW_OK:{check_password(password, u.password) if password else "SKIPPED"}\n')
        f.write(f'PW_HASH:{u.password[:60]}\n')
print('WROTE admin_verify.txt')
