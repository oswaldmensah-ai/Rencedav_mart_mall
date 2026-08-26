import requests
s = requests.Session()
base = 'http://127.0.0.1:8000'
# get home to populate cookies
r = s.get(base + '/')
print('GET / status', r.status_code)
print('cookies:', s.cookies.get_dict())
csrf = s.cookies.get('csrftoken') or ''
print('csrf from cookie:', csrf)
# try add product id 1
url = base + '/cart/add/1/'
resp = s.post(url, data={'quantity': '1'}, headers={'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest'})
print('POST', url, 'status', resp.status_code)
print('content-type:', resp.headers.get('content-type'))
print('response text:', resp.text[:2000])
