import os

from apps.accounts.models import User
email='florencedavor3@gmail.com'
password = os.environ.get('ADMIN_PASSWORD')
if not password:
	raise RuntimeError('Set ADMIN_PASSWORD before updating an administrator.')
u, created = User.objects.get_or_create(email=email, defaults={'first_name':'Florence','last_name':'Davor'})
u.set_password(password)
u.is_staff = True
u.is_superuser = True
u.is_admin = True
u.save()
print('SET', u.email, 'created=', created, 'flags=', u.is_staff, u.is_superuser, u.is_admin)
