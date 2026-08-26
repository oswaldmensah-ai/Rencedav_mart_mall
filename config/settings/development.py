"""
Development settings — verbose errors, debug toolbar, no HTTPS enforcement.
"""

from .base import *  # noqa
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', 'stifle-stays-probably.ngrok-free.dev']

# ─── ngrok Support ────────────────────────────────────────────────────────────
USE_X_FORWARDED_HOST = True
CSRF_TRUSTED_ORIGINS = [
    'https://stifle-stays-probably.ngrok-free.dev',
    'http://stifle-stays-probably.ngrok-free.dev',
]


# ─── Debug Toolbar ─────────────────────────────────────────────────────────────
INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
INTERNAL_IPS = ['127.0.0.1']

# (No ngrok/CSRF overrides in standard dev config.)



# ─── Email: print to console ───────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ─── Static Files ─────────────────────────────────────────────────────────
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# ─── Relaxed password hashing (faster in dev) ─────────────────────────────────
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
