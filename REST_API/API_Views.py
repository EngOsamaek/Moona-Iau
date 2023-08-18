from datetime import date

from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from Moona.models import Company, Customer, OrderTableView, OrdersList, VirtualOrder, Product, AdminSales, AdminProfit
from Moona.views import company_list, product_list


@csrf_exempt
@api_view(['GET'])
def block_company(request, id):
    company = Company.objects.get(id=id)
    if company.is_blocked:
        company.is_blocked = False
    else:
        company.is_blocked = True
    company.save()
    return redirect(company_list)


@csrf_exempt
@api_view(['GET'])
def block_products(request, id):
    product = Product.objects.get(id=id)
    if not product.is_available:
        product.is_available = True
        product.save()
    elif product.is_available:
        print(1)
        product.is_available = False
        product.save()
    return redirect(product_list(id=product.company.id))


"""For Customer Page"""

"""
def index(request):
    customerObj = Customer.objects.get(id=1)
    compound_total = 0
    total = 0
    prices = []
    products = []
    orders = OrdersList.objects.filter(customerID=customerObj)
    print(orders.all())
    for i in orders:
        products.append(VirtualOrder.objects.filter(orderNumber=i))

    for i in products:
        total = 0
        xx = None
        compound_total = 0
        if len(i) > 1:
            for x in i:
                obj = Product.objects.get(id=x.product_id)
                compound_total += obj.price * x.amount
                total = total + compound_total
                xx=x
            print(xx.orderNumber)
            objs = []
            orderTV = OrderTableView.objects.create(customer_ID=customerObj, orderNumber=xx.orderNumber, total=total,
                                                    date=date.today())
            orderTV.save()
        else:
            obj = Product.objects.get(id=i.get().product_id)
            total += obj.price * i.get().amount
            orderTV = OrderTableView.objects.create(customer_ID=customerObj, orderNumber=i.get().orderNumber,
                                                    total=total, date=date.today())
            orderTV.save()
    print(total)
    
    
    
    
    
    
    
    
     compound_total = 0
    prices = []

    products = []
    ids = []
    counter = 0
    orders = OrdersList.objects.filter(datetime=date.today())
    for i in orders:
        products.append(VirtualOrder.objects.filter(orderNumber=i))
        ids.append(i.customerID)
        print(i.orderNumber)

    for i in products:
        total = 0
        xx = None
        compound_total = 0
        if len(i) > 1:
            for x in i:
                obj = Product.objects.get(id=x.product_id)
                compound_total += obj.price * x.amount
                total = total + compound_total
                xx = x
            print(xx.orderNumber)
            orderTV = OrderTableView.objects.create(customer_ID=ids[counter], orderNumber=xx.orderNumber, total=total,date=date.today())
            orderTV.save()
            counter = counter + 1
        else:
            print(i.get().id)
            obj = Product.objects.get(id=i.get().product_id)
            total += obj.price * i.get().amount
            orderTV = OrderTableView.objects.create(customer_ID=ids[counter], orderNumber=i.get().orderNumber,total=total, date=date.today())
            orderTV.save()
            counter = counter + 1
    objs = OrderTableView.objects.filter(date=date.today())
    total = 0
    for i in objs:
        total = total + i.total
    try:
        salesTest = AdminSales.objects.get(date=date.today())
    except AdminSales.DoesNotExist:
        salesTest = None
    if salesTest is None:
        sales = AdminSales.objects.create(total=total, date=date.today())
        sales.save()
    else:
        salesTest.total = total

"""
