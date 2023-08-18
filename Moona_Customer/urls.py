"""Moona_Customer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Moona_Customer import views, API_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login1', API_views.login_method),
    path('register-page', API_views.register),
    path("registerCustomer", views.register),
    path('cartCustomer', views.show_cart),
    path('faqCustomer', views.faq),
    path("index", views.index),
    path("login", views.login),
    path('shopCustomer/<str:category>/<str:gender>/', views.shop, name='shop'),
    path('product-detail/<int:id>', views.product_detail),
    path('add-to-cart/<int:id>/<str:size>', views.add_to_cart),
    path('remove-from-cart/<int:id>/<str:size>', views.remove_from_cart),
    path('payment-page', views.payment_page),
    path("shopCustomer/<str:category>/", views.shop, name='shop_no_gender'),
    path('decrement/<int:id>/<str:size>', views.decrement_cart),
    path('increment/<int:id>/<str:size>', views.incremeant_cart),
    path("pay", views.pay),
    path('activate/<uidb64>/<token>', API_views.activate, name='activate'),
    path('verify-email/<int:user>/', API_views.verificationEmail, name='verification-email'),
    path('confirm_order', API_views.confirm_order),
    path('logout', API_views.logout_view),
    path('profile-page', views.profile_page),
    path('orders-page', views.orders_page),
    path('addresses-page', views.addresses_page),
    path('orders-details/<int:order_id>', views.order_details),
    path('address-edit/<int:id>', views.address_edit_page),
    path('address-update/<int:id>', views.address_update),
    path('address-add-page', views.address_add_page),
    path('address-add', views.address_add),
    path('profile-edit-page', views.profile_edit_page),
    path('profile-update', views.profile_update),
    path('review/<int:id>/<int:order>/<int:star>', views.review),
    path('remove-address/<int:id>',views.remove_address)
]
