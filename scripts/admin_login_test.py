import os, sys, django
from django.test import Client

sys.path.append(r'c:\rencedav_mart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.development')
django.setup()

c = Client()
email = 'florencedavor3@gmail.com'
pw = os.environ.get('ADMIN_PASSWORD')
if not pw:
    raise RuntimeError('Set ADMIN_PASSWORD before running this diagnostic.')
# Attempt to login via test client
logged_in = c.login(username=email, password=pw)
print('CLIENT_LOGIN', logged_in)
resp = c.get('/admin/')
print('ADMIN_STATUS', resp.status_code)
# Print a short snippet to confirm admin index content or login page
text = resp.content.decode('utf-8', errors='ignore')
if 'Django administration' in text and resp.status_code == 200:
    print('ADMIN_OK')
else:
    # check for login form marker
    if 'Please enter the correct' in text or 'username' in text.lower():
        print('ADMIN_NOT_AUTHENTICATED')
    else:
        print('ADMIN_OTHER')
print('SNIPPET:\n', text[:800])
