import datetime

from Moona.models import Sales, Invoice


def getTotalSale(request):
    total=Invoice.objects.all()
    sales=0
    for i in total:
        sales=sales+i.total

    obj=Sales.objects.create(date=datetime.datetime,total=sales)




