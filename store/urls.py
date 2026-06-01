from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Home and general pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Products
    path('products/', views.products_list_view, name='products_list'),
    path('products/<int:pk>/', views.product_detail_view, name='product_detail'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item_view, name='update_cart_item'),
    
    # Checkout and Orders
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/<int:pk>/confirmation/', views.order_confirmation_view, name='order_confirmation'),
    path('orders/', views.order_history_view, name='order_history'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    
    # Admin
path('dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
path('dashboard/products/', views.admin_products_view, name='admin_products'),
path('dashboard/orders/', views.admin_orders_view, name='admin_orders'),
]
