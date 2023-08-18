import json
import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Sum
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.datetime_safe import date
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from django.shortcuts import render
from datetime import datetime as ddt

from . import settings
from .forms import CompanyForm
from .models import OrdersList, Company_User
from Moona.models import Product, Company, Tokens, Invoice, AdminSales, OrdersList, AdminProfit, Customer, VirtualOrder, \
    OrderTableView, Address, products_images
from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def index(request):

    tokensObj = Tokens.objects.all()
    profit_total = 0
    total_sum_sales = 0
    total_sum_profit = 0
    sales = 0
    from datetime import timedelta
    today = ddt.today() - timedelta(days=1)

    orders = None
    cancelledOrders = 0
    orders_percentage = None
    orders_numbers = None
    try:
        orders = OrdersList.objects.filter(date__year=today.year, date__month=today.month)
        orders_numbers = len(orders.filter(date__day=today.day))
        if orders_numbers > 0:
            orders_percentage = orders_numbers / len(orders) * 100
        orders_percentage = 0
    except OrdersList.DoesNotExist:
        orders = None
    try:
        total = AdminSales.objects.filter(date__year=today.year, date__month=today.month)
        sales = total.get(date=date.today()).total

        sales_percentage = total.filter(date__year=today.year, date__month=today.month).aggregate(
            total_sum=Sum("total"))
        total_sum_sales = sales_percentage["total_sum"]
        if total_sum_sales:
            total_sum_sales = float(total_sum_sales)
            print(total_sum_sales)
        else:
            total_sum_sales = 0

        print(sales_percentage)

        total_sum_sales = total_sum_sales / len(total)
        total_sum_sales = sales / total_sum_sales * 100
    except AdminSales.DoesNotExist:
        sales = 0
        sales_percentage = 0
    try:
        profit = AdminProfit.objects.filter(date__year=today.year, date__month=today.month)
        profit_total = profit.get(date=date.today()).total
        profit_percentage = profit.filter(date__year=today.year, date__month=today.month).aggregate(
            total_sum=Sum("total"))
        total_sum_profit = profit_percentage["total_sum"]
        if total_sum_profit:
            total_sum_profit = float(total_sum_profit)
        else:
            total_sum_profit = 0

        total_sum_profit = total_sum_profit / len(profit)
        total_sum_profit = sales / total_sum_profit * 100
    except AdminProfit.DoesNotExist:
        profit_total = 0
        profit_percentage = 0
    try:
        cancelledOrders = len(
            OrdersList.objects.filter( date__year=today.year, date__month=today.month, date__day=today.day))
    except OrdersList.DoesNotExist:
        cancelledOrders = 0
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')

    return render(request, "index.html",
                  {"sales": sales, "tokens": tokensObj,
                   "profit": profit_total, "profit_percentage": total_sum_profit,
                   "sales_percentage": total_sum_sales, "orders": orders_numbers,
                   "orders_percentage": orders_percentage, "cancelled": cancelledOrders
                   })



from django.core.exceptions import ValidationError

def register_company(request):
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        company_name = request.POST.get('coName')
        company_type = request.POST.get('type')
        try:
            tax_no = int(request.POST.get('tax'))
        except ValueError:
            messages.error(request, 'Invalid Tax No. Please enter a valid number.')
            return render(request, 'page-register.html')
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")

        if Company.objects.filter(tax_no=tax_no).exists():
            messages.error(request, 'Tax No already exists. Please choose a different value.')
        elif Company.objects.filter(company_name=company_name).exists():
            messages.error(request, 'Company Name already exists. Please choose a different value.')
        else:
            new_company = Company(
                logo=logo,
                company_name=company_name,
                type=company_type,
                tax_no=tax_no,
            )
            new_company.save()

            if User.objects.filter(username=username).exists():
                messages.error(request,
                               'Username is already registered by another user, please choose another username.')
            else:
                userObj = User.objects.create_user(username=username, password=password,
                                                   email=email, is_staff=True, is_superuser=False)
                userObj.save()
                Company_User.objects.create(user_id=userObj.pk,company_id=new_company.pk)
                ab=Tokens.objects.create(id_id=new_company.pk,company_name=new_company.company_name)
                ab.save()
                sendWelcomeEmail(request,company_name,userObj.email)

                messages.success(request,
                                 'Company added successfully check the email \n which been sent to activate your account.')
            return render(request, 'page-register.html')
    return render(request, 'page-register.html')


def open_register(request):
    return render(request,"page-register.html")


def product_list(request, id):
    if not request.user.is_superuser:
        print(request.user.is_superuser)
        return HttpResponseForbidden('Access denied')
    products = None
    imgs = None
    if id == 0:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(company=Company.objects.get(id=id))

    companies = Company.objects.raw("select * from company inner join product on company.id=product.company_id ")
    imgs = products_images.objects.raw(
        "select image from products_images inner join product on products_images.id=product.id ")
    print(companies)
    companies = list(set(companies))
    return render(request, 'product-list(admin).html', {'products': products, "companies": companies, "imgs": imgs})

def co_product_list(request):
    if  request.user.is_superuser :
        print(request.user.is_superuser)
        return HttpResponseForbidden('Access denied')
    company_id=Company_User.objects.get(user_id=request.user.id).company
    print(company_id.id)
    imgs=[]
    products=Product.objects.filter(company_id=company_id)
    for i in products:
        imgs.append(products_images.objects.filter(image_id=i).first())
    print(company_id.id)

    return render(request,"product-list(company).html",{"products":products,"imgs":imgs})

def company_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden('Access denied')
    companies = Company.objects.all()

    return render(request, 'company-list.html', {'companies': companies})


def loginadmin(request):
    return render(request, 'page-login.html')

def check_admin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("hello")
            login(request, user)
            print(password)
        return redirect("/admin")

def co_login_page(request):
    return render(request,"page-login(Company).html")

def check_company(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("hello")
            login(request, user)
            print(password)
        return redirect("/co-home")

def co_index(request):

    if not request.user.is_authenticated:
        redirect("/co-login")
    tokensObj = Tokens.objects.all()
    profit_total = 0
    total_sum_sales = 0
    total_sum_profit = 0
    sales = 0
    from datetime import timedelta
    today = ddt.today() - timedelta(days=1)

    orders = None
    cancelledOrders = 0
    orders_percentage = None
    orders_numbers = None
    try:
        orders = OrdersList.objects.filter(date__year=today.year, date__month=today.month)
        orders_numbers = len(orders.filter(date__day=today.day))
        if orders_numbers > 0:
            orders_percentage = orders_numbers / len(orders) * 100
        orders_percentage = 0
    except OrdersList.DoesNotExist:
        orders = None
    try:
        total = AdminSales.objects.filter(date__year=today.year, date__month=today.month)
        sales = total.get(date=date.today()).total

        sales_percentage = total.filter(date__year=today.year, date__month=today.month).aggregate(
            total_sum=Sum("total"))
        total_sum_sales = sales_percentage["total_sum"]
        if total_sum_sales:
            total_sum_sales = float(total_sum_sales)
            print(total_sum_sales)
        else:
            total_sum_sales = 0

        print(sales_percentage)

        total_sum_sales = total_sum_sales / len(total)
        total_sum_sales = sales / total_sum_sales * 100
    except AdminSales.DoesNotExist:
        sales = 0
        sales_percentage = 0
    try:
        profit = AdminProfit.objects.filter(date__year=today.year, date__month=today.month)
        profit_total = profit.get(date=date.today()).total
        profit_percentage = profit.filter(date__year=today.year, date__month=today.month).aggregate(
            total_sum=Sum("total"))
        total_sum_profit = profit_percentage["total_sum"]
        if total_sum_profit:
            total_sum_profit = float(total_sum_profit)
        else:
            total_sum_profit = 0

        total_sum_profit = total_sum_profit / len(profit)
        total_sum_profit = sales / total_sum_profit * 100
    except AdminProfit.DoesNotExist:
        profit_total = 0
        profit_percentage = 0
    try:
        cancelledOrders = len(
            OrdersList.objects.filter( date__year=today.year, date__month=today.month, date__day=today.day))
    except OrdersList.DoesNotExist:
        cancelledOrders = 0

    return render(request, "indexCompany.html",
                  {"sales": sales, "tokens": tokensObj,
                   "profit": profit_total, "profit_percentage": total_sum_profit,
                   "sales_percentage": total_sum_sales, "orders": orders_numbers,
                   "orders_percentage": orders_percentage, "cancelled": cancelledOrders
                   })

@csrf_exempt
def product_edit(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product-edit.html', {'product': product})








@csrf_exempt
def product_update(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST' and request.FILES['image']:
        product_name = request.POST['product_name']
        price = request.POST['price']
        image = request.FILES['image']
        amount = request.POST['amount']

        product.product_name = product_name
        product.price = price
        product.image = image
        product.amount = amount

        product.save()

        return redirect(product_list)
    return render(request, 'product-edit.html', {"product": product})


@csrf_exempt
def product_add(request):
    if request.method == 'POST' and request.FILES['image']:
        product_name = request.POST['product_name']
        price = request.POST['price']
        image = request.FILES.getlist('image')
        amount = request.POST['amount']
        product = Product.objects.create(product_name=product_name, price=price, amount=amount,
                                         company_id=3, is_available=True)
        product.save()
        if len(image) > 1:
            for i in image:
                images = products_images.objects.create(image_id=product, image="media/"+str(i))
                images.save()
        else:
            images = products_images.objects.create(image_id=product, image="media/"+str(image[0]))
            images.save()
        return redirect(product_list, 0)
    return render(request, 'product-add.html')



@csrf_exempt
def product_delete(request, id):
    obj = Product.objects.get(id=id)

    obj.delete()

    return redirect("product-list")


from datetime import datetime
from .models import OrdersList

from django.core.paginator import Paginator


def reports_sales(request):

    from_date = request.GET.get('from', None)
    to_date = request.GET.get('to', None)
    orders_list = OrdersList.objects.all()

    if from_date or to_date:
        try:
            if from_date:
                from_date = datetime.strptime(from_date, "%Y-%m-%d")
                orders_list = orders_list.filter(date__gte=from_date)
            if to_date:
                to_date = datetime.strptime(to_date, "%Y-%m-%d")
                orders_list = orders_list.filter(date__lte=to_date)
        except ValueError as e:
            raise Http404("Invalid date format. Date should be in YYYY-MM-DD format.") from e

    orders_list = orders_list.order_by('-date')

    paginator = Paginator(orders_list, 10)  # Show 10 orders per page

    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    return render(request, "report-page.html", {"orders": orders})

def generate_report(request):

    if request.method == 'POST':
        from_date = request.POST.get('from', None)
        to_date = request.POST.get('to', None)
        orders_list = OrdersList.objects.all()

        if from_date or to_date:
            try:
                if from_date:
                    from_date = datetime.strptime(from_date, "%Y-%m-%d")
                    orders_list = orders_list.filter(date__gte=from_date)
                if to_date:
                    to_date = datetime.strptime(to_date, "%Y-%m-%d")
                    orders_list = orders_list.filter(date__lte=to_date)
            except ValueError as e:
                raise Http404("Invalid date format. Date should be in YYYY-MM-DD format.") from e

        orders_list = orders_list.order_by('-date')


        return generate_pdf(orders_list)  # Return the response from generate_pdf
    else:
        print("Error")
        return redirect("/reports")



from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table

# ...
from matplotlib.dates import date2num

def generate_pdf(orders):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Add logo
    logo_path = "media/moona-logo.png"
    img = Image(logo_path, width=200, height=150)
    elements.append(img)

    # Add text
    styles = getSampleStyleSheet()
    ptext = 'Based on the Admin Request, we generated this report.'
    elements.append(Paragraph(ptext, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add table with order data
    data = [['Order Number', 'Status', 'Date', 'Customer ID', 'Total']]
    for order in orders:
        if order.status:
            order.status="Delivered"
        else:
            order.status="Under progress"
        row = [order.orderNumber, order.status, order.date, order.customerID.customer_name, order.total]
        data.append(row)
    table = Table(data)
    elements.append(table)
    elements.append(Spacer(1, 12))

    # Calculate total profit
    total_profit = sum(order.total for order in orders)
    ptext = f'Total Profit: {total_profit}'
    elements.append(Paragraph(ptext, styles['Normal']))

    # Add a line chart
    fig, ax = plt.subplots()
    order_dates = [date2num(order.date) for order in orders]  # Convert dates to numeric format for matplotlib
    order_totals = [order.total for order in orders]
    ax.plot_date(order_dates, order_totals, color='blue', fmt='-')  # Plot dates on the x-axis
    ax.set_xlabel('Date')
    ax.set_ylabel('Total')
    ax.set_title('Order Totals')
    plt.tight_layout()

    imgdata = BytesIO()
    fig.savefig(imgdata, format='png')
    imgdata.seek(0)
    imgss = Image(imgdata, 500, 200)
    elements.append(imgss)

    # Build the pdf
    doc.build(elements)

    # Return the pdf as a response
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')

def get_tokens(request):
    tokens = Tokens.objects.all()
    if not tokens.exists():
        return redirect("/admin")

    return render(request, "tokens.html", {"tokens": tokens})

def activate_company(request,id):
    user_id=Company_User.objects.get(company_id=id)
    user=User.objects.get(id=user_id.user.id)
    user.is_active=True
    user.save()
    tk=Tokens.objects.get(id_id=id)
    tk.delete()
    return redirect("/company-requests")



def sendWelcomeEmail(request, name, email):
    current_site = get_current_site(request)
    email_subject = "Confirm your email!"
    message2 = render_to_string('email_confirmation.html', {

        'name': name,
        'domain': current_site.domain,
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = True
    email.send()
    pass


def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/admin-login')

def logout_co(request):
    logout(request)
    return redirect('/co-login')
