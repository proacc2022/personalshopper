from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('password/', views.user_password, name='user_password'),
    path('updateprofile/', views.user_update, name='updateprofile'),
    path('manageaddress/', views.user_addressupdate, name='user_addressupdate'),
    path('managecontact/', views.user_contactupdate, name='user_contactupdate'),
    path('orders/', views.user_orders, name='user_orders'),
    path('orders_product/', views.user_order_product, name='user_order_product'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('managepayment/creditcards/', views.ccuser_managepayment, name='ccuser_payment'),
    path('managepayment/debitcards/', views.dcuser_managepayment, name='dbuser_payment'),
    path('managepayment/upi/', views.user_upimanagepayment, name='upiuser_payment'),
    path('managepayment/paytm/', views.user_paytmmanagepayment, name='paytmuser_payment'),
    path('managepayment/', views.user_managepayment, name='user_payment'),

]
