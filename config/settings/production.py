"""
Production settings — strict security, real DB URL, S3 media.
"""

from .base import *  # noqa
from decouple import config
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [host.strip() for host in config('ALLOWED_HOSTS', default='').split(',') if host.strip()]
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if origin.strip()]

# ─── Database via DATABASE_URL env var ─────────────────────────────────────────
DATABASES['default'] = dj_database_url.config(  # noqa: F405
    env='DATABASE_URL',
    conn_max_age=600,
    ssl_require=True,
)

# ─── Security Headers ──────────────────────────────────────────────────────────
SECURE_BROWSER_XSS_FILTER       = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_HSTS_SECONDS             = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_PRELOAD             = True
SECURE_SSL_REDIRECT             = True
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
X_FRAME_OPTIONS                 = 'DENY'

# ─── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND    = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST       = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT       = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS    = True
EMAIL_HOST_USER  = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@rencedavmart.com')

# ─── Static Files for Production ────────────────────────────────────────────────
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─── Static / Media via AWS S3 (uncomment when ready) ─────────────────────────
# DEFAULT_FILE_STORAGE    = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE     = 'storages.backends.s3boto3.S3StaticStorage'
# AWS_ACCESS_KEY_ID       = config('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY   = config('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME      = 'us-east-1'
# AWS_S3_CUSTOM_DOMAIN    = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
