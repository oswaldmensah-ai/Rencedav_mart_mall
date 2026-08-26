import os

from django.http import HttpResponse
from django.contrib.auth import authenticate
from apps.accounts.models import User


def auth_debug(request):
    email = request.GET.get('email', 'florencedavor3@gmail.com')
    password = request.GET.get('pw') or os.environ.get('ADMIN_PASSWORD', '')
    setpw = request.GET.get('setpw')
    u = User.objects.filter(email=email).first()
    if not u:
        return HttpResponse('NOTFOUND', content_type='text/plain')
    if setpw:
        u.set_password(password)
        u.save()
    out = []
    out.append(f'EMAIL:{u.email}')
    out.append(f'IS_STAFF:{u.is_staff}')
    out.append(f'IS_SUPERUSER:{u.is_superuser}')
    out.append(f'IS_ADMIN:{u.is_admin}')
    out.append(f'IS_ACTIVE:{u.is_active}')
    out.append('PW_OK:'+str(u.check_password(password)))
    a = authenticate(request, username=email, password=password)
    out.append('AUTH:'+str(bool(a)))
    return HttpResponse('\n'.join(out), content_type='text/plain')
