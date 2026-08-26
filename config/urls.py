from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # ── Built-in Admin ────────────────────────────────────────────────────────
    path('admin/', admin.site.urls),  # <--- 2. Add this line inside your urlpatterns

    # ── Storefront ────────────────────────────────────────────────────────────
    path('',                  include('apps.store.urls',    namespace='store')),
    path('cart/',             include('apps.cart.urls',     namespace='cart')),
    path('orders/',           include('apps.orders.urls',   namespace='orders')),
    path('payments/',         include('apps.payments.urls', namespace='payments')),

    # ── Accounts ─────────────────────────────────────────────────────────────
    path('accounts/',         include('apps.accounts.urls', namespace='accounts')),
    path('accounts/',         include('allauth.urls')),

    # ── Admin Dashboard ───────────────────────────────────────────────────────
    path('dashboard/',        include('apps.dashboard.urls', namespace='dashboard')),
]

# ── Debug Toolbar (dev only) ──────────────────────────────────────────────────
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)