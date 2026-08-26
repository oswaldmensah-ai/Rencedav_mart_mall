from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.order_create, name='order_create'),
    path('confirmation/', views.order_created, name='order_created'),
]