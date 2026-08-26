from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # The storefront homepage showing category lists and items
    path('', views.home, name='home'),
    path('products/', views.home, name='products'),
    path('search/', views.search, name='search'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('products/all/', views.products_all, name='products_all'),

    # Detailed landing page for a specific product using its unique slug text
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]