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
logged_in = c.login(username=email, password=pw)
resp = c.get('/admin/')
text = resp.content.decode('utf-8', errors='ignore')
with open(r'c:\rencedav_mart\admin_client_debug.txt','w', encoding='utf-8') as f:
    f.write(f'CLIENT_LOGIN:{logged_in}\n')
    f.write(f'ADMIN_STATUS:{resp.status_code}\n')
    f.write('ADMIN_OK:'+str('Django administration' in text and resp.status_code==200)+'\n')
    f.write('SNIPPET:\n')
    f.write(text[:400])
print('WROTE')
