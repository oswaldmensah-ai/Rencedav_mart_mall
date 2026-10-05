"""
Development settings — verbose errors, debug toolbar, no HTTPS enforcement.
"""

from .base import *  # noqa
from decouple import config

DEBUG = True

ALLOWED_HOSTS = [
    host.strip()
    for host in config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0').split(',')
    if host.strip()
]

# Allow forwarded host headers only when explicitly configured for a proxy or tunnel.
USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST', default=False, cast=bool)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in config('CSRF_TRUSTED_ORIGINS', default='').split(',')
    if origin.strip()
]


# ─── Debug Toolbar ─────────────────────────────────────────────────────────────
INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
INTERNAL_IPS = ['127.0.0.1']



# ─── Email: print to console ───────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ─── Static Files ─────────────────────────────────────────────────────────
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# ─── Relaxed password hashing (faster in dev) ─────────────────────────────────
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
