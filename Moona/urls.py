from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import Moona.views
from Moona import views, settings
from REST_API import API_Views
from Moona_Customer import views as views2


urlpatterns = [
    path('', include('Moona_Customer.urls')),
    path('', views2.index),
    path('admin',views.index),
    path('reports', views.reports_sales),
    path('company-list', views.company_list),
    path('product-list/<int:id>', views.product_list),
    path('product-edit', views.product_edit),
    path('product-delete/<int:id>', API_Views.block_products),
    path('product-update/<int:id>', views.product_update),
    path('product-edit/<int:id>', views.product_edit),
    path('product-edit/product-update/<int:id>', views.product_update),
    path('product-add', views.product_add),
    path("isblock/<int:id>",API_Views.block_company),
    path("register",views.open_register),
    path("company_register",views.register_company),
    path('generate-report',views.generate_report),
    path('company-requests',views.get_tokens),
    path('token-accept/<int:id>',views.activate_company),
    path('admin-login',Moona.views.loginadmin),
    path('check-login',Moona.views.check_admin),
    path('complete-register',Moona.views.register_company),
    path("co-products-list",Moona.views.co_product_list),
    path("co-home",Moona.views.co_index),
    path("check_company",Moona.views.check_company),
    path("co-login",Moona.views.co_login_page),
    path('admin-logout',views.logout_view),
    path('company-logout',views.logout_co),

              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


