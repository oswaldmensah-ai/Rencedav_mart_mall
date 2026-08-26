from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.overview, name='overview'),
    path('categories/add/', views.add_category, name='add_category'),
    path('products/add/', views.add_product, name='add_product'),
    path('orders/<int:order_id>/review/', views.review_order, name='review_order'),
]
