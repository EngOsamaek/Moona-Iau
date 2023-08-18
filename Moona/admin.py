from django.contrib import admin
from .models import (Company, Product, ProductSize, products_images, Tokens, Customer,
                     Address, OrdersList, VirtualOrder, OrderTableView,
                     Company_orders_list, Company_VirtualOrder, AdminSales,
                     AdminProfit, Cart, GenderProducts)


admin.site.register(Company)
admin.site.register(Product)
admin.site.register(ProductSize)
admin.site.register(products_images)
admin.site.register(Tokens)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(OrdersList)
admin.site.register(VirtualOrder)
admin.site.register(OrderTableView)
admin.site.register(Company_orders_list)
admin.site.register(Company_VirtualOrder)

admin.site.register(AdminSales)
admin.site.register(AdminProfit)
admin.site.register(Cart)
admin.site.register(GenderProducts)
