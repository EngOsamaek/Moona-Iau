import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from Auth.tokens import generate_token
import Moona_Customer
from Moona import settings
from Moona.models import Customer, Product, Company, products_images, Address, Cart, OrderTableView, VirtualOrder, \
    OrdersList
from Moona_Customer.views import index


@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        data = request.POST

        # Split the address into its components
        address_parts = data.get('address').split('-')
        if len(address_parts) != 8:
            messages.error(request, "Invalid address format")
            return JsonResponse({"status": "error"})

        # Assign each part of the address to a variable
        country = address_parts[0]
        city = address_parts[1]
        district = address_parts[2]
        neighborhood = address_parts[3]
        street_name = address_parts[4]
        street_number = address_parts[5]
        building_number = address_parts[6]
        flat_number = address_parts[7]

        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        password = data.get('password')
        tc_no = data.get('tc_no')
        gender = data.get('gender')
        b_day = data.get('b_day')
        phone = data.get('phone')

        # Check if the user already exists before creating a new one
        if User.objects.filter(username=email).exists():
            messages.error(request, "The email you entered has been registered before")
            return JsonResponse({"status": "error"})

        # Create the user account
        user = User.objects.create_user(username=email, password=password, email=email)
        user.first_name = name
        user.last_name = surname
        user.is_active = False

        # Create the customer
        if user.save():
            customer = Customer.objects.create(
                id_id=user,
                customer_name=name + " " + surname,
                customer_TC=tc_no,
                customer_gender=gender,
                customer_birthdate=b_day,
                customer_phone=phone
                )
            address = Address.objects.create(
                customerId=customer,
                country=country,
                city=city,
                district=district,
                neighbourhood=neighborhood,
                streetName=street_name,
                streetNumber=street_number,
                doorNumber=str(building_number) + str(flat_number)
            )

        # Create the address

        messages.success(request, "Registration successful!")
        verificationEmail(request, user)
        return JsonResponse({"status": "success"})

    return redirect("registerCustomer")


@csrf_exempt
def login_method(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(password)
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print("hello")
            login(request, user)
            print(password)
            return redirect(Moona_Customer.views.index)
        else:

            return render(request, 'loginCustomer.html', {'error_message': 'Invalid login credentials'})


def verificationEmail(request, myuser):
    current_site = get_current_site(request)
    email_subject = "Confirm your email!"
    message2 = render_to_string('email_confirmation.html', {
        'name': myuser.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        'token': generate_token.make_token(myuser)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
    )
    email.content_subtype = "html"
    email.fail_silently = False
    try:
        email.send()
    except Exception as e:
        print("Error sending email: ", e)
    pass


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        messages.success(request, "Your Account has been activated!!")
        return redirect("/login")


class Cart_details:
    def __init__(self):
        self.product_id = None
        self.product_name = None
        self.product_price = None
        self.product_amount = None
        self.product_image = None
        self.total = 0.0
def confirm_order(request):
    cartObjs = Cart.objects.filter(customer=request.user)
    products = []
    total = 0.0
    for i in cartObjs:
        product_dict = {
            "product_id": i.product.id,
            "product_name": i.product.product_name,
            "product_image": "/" + str(products_images.objects.filter(image_id=i.product.id).first().image),
            "product_amount": i.amount,
            "product_price": i.product.price,
            "total": i.product.price * i.amount,
        }
        products.append(product_dict)
        i.delete()
    for product in products:
        total += product["total"]

    current_site = get_current_site(request)
    myuser = request.user
    email_subject = "Your order been confirmed!"
    address = Address.objects.filter(customerId=Customer.objects.get(id_id=myuser)).first()
    address_components = [
        str(address.country),
        str(address.city),
        str(address.district),
        str(address.neighbourhood),
        str(address.streetName),
        str(address.streetNumber),
        str(address.doorNumber)
    ]
    address_string = "-".join(address_components)
    message2 = render_to_string('confirm_order.html', {
        'address': address_string,
        'name': myuser.first_name,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
        'token': generate_token.make_token(myuser),
        'products': products,
        'total': (total + 50)
    })
    email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
    )
    email.content_subtype = "html"
    email.fail_silently = False
    try:
        email.send()
        return redirect("/index")
    except Exception as e:
        print("Error sending email: ", e)
        return redirect('/payment-page')

@login_required
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/login')





