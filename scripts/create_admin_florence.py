import os

from apps.accounts.models import User
email = 'florencedavor3@gmail.com'
password = os.environ.get('ADMIN_PASSWORD')
if not password:
	raise RuntimeError('Set ADMIN_PASSWORD before creating an administrator.')
user, created = User.objects.get_or_create(email=email, defaults={'first_name':'Florence','last_name':'Davor'})
user.set_password(password)
user.is_staff = True
user.is_superuser = True
user.is_admin = True
user.save()
print('SUPERUSER', user.email, 'created=', created)
