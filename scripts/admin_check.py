from django.conf import settings
from django.contrib.auth.hashers import check_password
from apps.accounts.models import User
email='florencedavor3@gmail.com'
u=User.objects.filter(email=email).first()
with open(r'c:\rencedav_mart\admin_debug.txt','w', encoding='utf-8') as f:
    if not u:
        f.write('NOTFOUND')
    else:
        f.write(f'EMAIL:{u.email}\n')
        f.write(f'IS_STAFF:{u.is_staff}\n')
        f.write(f'IS_SUPERUSER:{u.is_superuser}\n')
        f.write(f'IS_ADMIN:{u.is_admin}\n')
        f.write(f'IS_ACTIVE:{u.is_active}\n')
            password = os.environ.get('ADMIN_PASSWORD')
            f.write('PW_OK:'+str(check_password(password, u.password) if password else 'SKIPPED')+'\n')
        f.write('PW_HASH:'+u.password+'\n')
        f.write('BACKENDS:'+str(settings.AUTHENTICATION_BACKENDS)+'\n')
print('wrote')
