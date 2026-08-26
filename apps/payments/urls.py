from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initiate/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
    path('simulator/', views.webhook_simulator, name='webhook_simulator'),
]
