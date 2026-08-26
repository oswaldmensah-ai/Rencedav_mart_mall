from django.urls import path
from . import views
from .views_order import order_history, order_detail

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register,    name='register'),
    path('login/',    views.login_view,  name='login'),
    path('logout/',   views.logout_view, name='logout'),
    path('profile/',  views.profile,     name='profile'),
    path('profile/orders/', order_history, name='order_history'),
    path('profile/orders/<int:order_id>/', order_detail, name='order_detail'),
]
