from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.registerUser, name="register"),
    path('login-otp/', views.request_otp, name='request_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('product/<int:product_id>/', views.product_detail, name="product_detail"),
    path('checkout/<int:product_id>/', views.checkout, name="checkout"),
    path('payment/<int:product_id>/', views.payment, name="payment"),
    path('order-success/', views.order_success, name="order_success"),
    path('my-orders/', views.my_orders, name="my_orders"),
    path('sales-report/', views.sales_report, name="sales_report"),
]