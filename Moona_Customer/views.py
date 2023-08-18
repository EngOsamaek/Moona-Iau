import datetime

import stripe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
import pandas as pd
from django.http import JsonResponse
import json
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from Moona import settings
from Moona.models import Product, products_images, ProductSize, Cart, GenderProducts, Customer, Address, VirtualOrder, \
    OrdersList, OrderTableView
from Moona.forms import SearchForm

from django.db.models import Avg


class Recommender:
    DATA_COLS = ['orderNumber_id', 'product_id', 'rating']
    MEASURES = ['RMSE']
    FILTER_COLS = ['orderNumber_id', 'product_id', 'rating']

    def __init__(self):
        print("Loading data...")
        queryset = VirtualOrder.objects.values(*self.DATA_COLS)
        self.df = pd.DataFrame.from_records(queryset)
        self.reader = Reader()
        self.data = Dataset.load_from_df(self.df[self.FILTER_COLS], self.reader)
        self.svd = SVD()
        cross_validate(self.svd, self.data, measures=self.MEASURES, cv=5, verbose=True)
        self.trainset = self.data.build_full_trainset()
        self.svd.fit(self.trainset)
        self.all_product_ids = self.df['product_id'].unique()

    def recommend_products(self, orderNumber_id, num_recommendations=5):
        print("Recommending products...")
        predictions = [(product_id, self.svd.predict(str(orderNumber_id), str(product_id)).est)
                       for product_id in self.all_product_ids]
        predictions.sort(key=lambda x: x[1], reverse=True)

        top_recommendations = [
                                  (product_id, predicted_rating) for product_id, predicted_rating in predictions
                                  if self.df[(self.df['orderNumber_id'] == orderNumber_id) &
                                             (self.df['product_id'] == product_id)].empty
                              ][:num_recommendations]

        for product_id, predicted_rating in top_recommendations:
            print(f"Product ID: {product_id}, Predicted Rating: {predicted_rating}")

        return top_recommendations


class ProductObj:
    def __init__(self, product, image, sizes, average_rating):
        self.id = product.id
        self.name = product.product_name
        self.price = product.price
        self.url = image.image
        self.size = sizes if sizes else "STD"
        self.rate = average_rating


def index(request):
    products = Product.objects.filter(amount__gt=0)
    product_images = products_images.objects.filter(image_id__in=products.values_list('id', flat=True))

    categories = ['Fashion', 'Decoration', 'Electronics']
    images_dict = {category: [] for category in categories}

    for category in categories:
        category_products = products.filter(category=category)
        for product in category_products:
            sizes = ProductSize.objects.filter(product=product).values_list('size', flat=True)
            image = product_images.filter(image_id=product.id).first()
            average_rating_aggregate = VirtualOrder.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            average_rating = round(average_rating_aggregate) if average_rating_aggregate is not None else None
            images_dict[category].append(ProductObj(product, image, sizes, average_rating))
    tops = []
    try:
        recommender = Recommender()
        top_2_recommendations = recommender.recommend_products(request.user.id)

        for product_id, _ in top_2_recommendations:
            product = Product.objects.get(id=product_id)
            image = product_images.filter(image_id=product.id).first()
            average_rating = VirtualOrder.objects.filter(product=product_id).aggregate(Avg('rating'))['rating__avg']
            tops.append(ProductObj(product, image, [], average_rating))
    except (Product.DoesNotExist, products_images.DoesNotExist):
        print("Product or product images not found")

    return render(request, 'indexCustomer.html', {
        "images": images_dict['Fashion'] + images_dict['Decoration'] + images_dict['Electronics'],
        "fashion_img": images_dict['Fashion'],
        "decoration_img": images_dict['Decoration'],
        "electronics_img": tops,
    })


def login(request):
    return render(request, 'loginCustomer.html')


class Shop:
    def __init__(self, product, images, sizes, average_rating):
        self.id = product.id
        self.name = product.product_name
        self.price = product.price
        self.category = product.category
        self.size = sizes if sizes else "STD"
        self.images = images
        self.average_rating = average_rating

from django.core.paginator import Paginator

def shop(request, category, gender=None):
    search_term = request.POST.get('searchEng')

    gender = gender.lower() if gender else None
    gender = {'true': True, 'false': False}.get(gender)

    if category == "all":
        products = Product.objects.filter(amount__gt=0)
    else:
        products = Product.objects.filter(category=category, amount__gt=0)

    if gender is not None:
        product_ids = GenderProducts.objects.filter(gender=gender, product__amount__gt=0).values_list('product__id',
                                                                                                      flat=True)
        products = products.filter(id__in=product_ids)

    if search_term:
        products = products.filter(Q(product_name__icontains=search_term))

    objects = []
    for product in products:
        sizes = ProductSize.objects.filter(product=product).values_list('size', flat=True)
        images = products_images.objects.filter(image_id=product.id)[:2]
        image_urls = ["/" + str(image.image) for image in images]
        average_rating = VirtualOrder.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
        objects.append(Shop(product, image_urls, sizes, average_rating))

    paginator = Paginator(objects, 10)

    page_number = request.GET.get('page')

    products_page = paginator.get_page(page_number)

    return render(request, 'shopCustomer.html',
                  {"products": products_page, "current_category": category, "current_gender": gender})



def register(request):
    return render(request, 'registerCustomer.html')


def cart(request):
    return render(request, 'cartCustomer.html')


def faq(request):
    return render(request, 'faqCustomer.html')



class ProductDetails:
    def __init__(self):
        self.id = None
        self.productName = None
        self.productPrice = None
        self.productSizes = []
        self.images = []
        self.productColors = []


@login_required
def product_detail(request, id):
    obj = ProductDetails()

    try:
        product = Product.objects.get(id=id)
        images = products_images.objects.filter(image_id=id)
        sizes = ProductSize.objects.filter(product=id)

        obj.id = product.id
        obj.productName = product.product_name
        obj.productPrice = product.price
        for i in sizes:
            obj.productSizes.append(i.size)
        for i in images:
            obj.images.append("/" + str(i.image))
        if sizes.first() is None:
            obj.productSizes.append("STD")
        print(obj.productSizes[0])
    except Product.DoesNotExist:
        pass

    return render(request, "shop-details-1.html", {"product": obj})


@login_required
def add_to_cart(request, id, size):
    product_obj = Product.objects.get(id=id)
    customer_obj = User.objects.get(id=request.user.id)
    try:
        product_size_obj = ProductSize.objects.get(product=product_obj, size=size)
    except ProductSize.DoesNotExist:
        product_size_obj = ProductSize.objects.create(product=product_obj, size=size, amount=product_obj.amount)

    cart = None
    try:
        cart = Cart.objects.get(product=product_obj, customer=customer_obj, product_sizes=product_size_obj)
        cart.amount = cart.amount + 1
        cart.save()
    except Cart.DoesNotExist:
        cart = Cart.objects.create(product=product_obj, customer=customer_obj, amount=1, product_sizes=product_size_obj)
        cart.save()

    return redirect("/cartCustomer")


@login_required
def remove_from_cart(request, id, size=None):
    print(id)
    product_obj = Product.objects.get(id=id)
    customer_obj = User.objects.get(id=request.user.id)
    product_size_obj = ProductSize.objects.get(product=product_obj, size=size)

    try:
        cart = Cart.objects.get(product=product_obj, customer=customer_obj, product_sizes=product_size_obj)
        cart.delete()
    except Cart.DoesNotExist:
        print(11)
    return redirect('/cartCustomer')


@login_required
def decrement_cart(request, id, size):
    print(id)
    product_obj = Product.objects.get(id=id)
    customer_obj = User.objects.get(id=request.user.id)
    prd = ProductSize.objects.get(product=product_obj, size=size)
    try:
        cart = Cart.objects.get(product=product_obj, customer=customer_obj, product_sizes=prd)
        if cart.amount > 1:
            cart.amount = cart.amount - 1
            cart.save()
        else:
            cart.delete()
    except Cart.DoesNotExist:
        print(11)
    return redirect('/cartCustomer')


@login_required
def incremeant_cart(request, id, size):
    print(id)
    product_obj = Product.objects.get(id=id)
    customer_obj = User.objects.get(id=request.user.id)
    prd = ProductSize.objects.get(product=product_obj, size=size)
    try:
        cart = Cart.objects.get(product=product_obj, customer=customer_obj, product_sizes=prd)
        cart.amount = cart.amount + 1
        cart.save()

    except Cart.DoesNotExist:
        print(11)
    return redirect('/cartCustomer')


class Cart_details:
    def __init__(self):
        self.product_id = None
        self.product_name = None
        self.product_price = None
        self.product_amount = None
        self.product_image = None
        self.total = 0.0
        self.size = None
        self.rate = None


@login_required
def show_cart(request):
    cart = Cart.objects.filter(customer=request.user)
    products = []
    total = 0.0
    for i in cart:
        obj = Cart_details()
        obj.product_id = i.product.id
        obj.product_name = i.product.product_name
        obj.product_image = "/" + str(products_images.objects.filter(image_id=i.product.id).first().image)
        obj.product_amount = i.amount
        obj.product_price = i.product.price
        obj.total = obj.product_price * obj.product_amount
        obj.size = i.product_sizes.size
        products.append(obj)
    for i in products:
        total = total + i.total
    return render(request, "cartCustomer.html", {"products": products, "subtotal": total, "total": (total + 50)})


@login_required
def payment_page(request):
    cart = Cart.objects.filter(customer=request.user)
    products = []
    total = 0.0
    for i in cart:
        obj = Cart_details()
        obj.product_id = i.product.id
        obj.product_name = i.product.product_name
        obj.product_image = "/" + str(products_images.objects.filter(image_id=i.product.id).first().image)
        obj.product_amount = i.amount
        obj.product_price = i.product.price
        obj.total = obj.product_price * obj.product_amount
        products.append(obj)
    for i in products:
        total = total + i.total
    return render(request, 'paymentCustomer.html', {"total": (total + 50)})


stripe.api_key = settings.STRIPE_SECRET_KEY


def pay(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        card_number = data.get('card_number')
        exp_month = data.get('exp_month')
        exp_year = data.get('exp_year')
        cvc = data.get('cvc')

        try:
            # Create Stripe token
            token = stripe.Token.create(
                card={
                    "number": card_number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc
                }
            )

            # Create Stripe charge
            charge = stripe.Charge.create(
                amount=1000,  # Amount in cents
                currency='usd',
                source=token.id,
                description='Example Charge'
            )
            register_order(request)
            return JsonResponse({"message": "Payment successful, check your email for order details"}, status=200)

        except stripe.error.CardError as e:
            return JsonResponse({"message": "Payment Failed: " + e.error.message}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)


def register_order(request):
    last_order = OrdersList.objects.all().order_by('-orderNumber').first()
    if last_order:
        new_order_number = last_order.orderNumber + 1
    else:
        new_order_number = 1

    order_list = OrdersList.objects.create(
        orderNumber=new_order_number,
        status="0",
        date=datetime.datetime.now(),
        customerID=request.user.customer,
        total=0
    )
    order_list.save()
    total = 0.0
    # Create a VirtualOrder object
    carts = Cart.objects.filter(customer=request.user)
    for cart in carts:
        try:
            VO = VirtualOrder.objects.get(orderNumber=order_list,product=cart.product)
            VO.amount = VO.amount + cart.amount
        except VirtualOrder.DoesNotExist:
            virtual_order = VirtualOrder.objects.create(
                orderNumber=order_list,
                product=cart.product,
                amount=cart.amount,
                rating=0
            )

        prd = cart.product_sizes
        prd.amount = prd.amount - cart.amount
        prd.save()
        total = total + cart.amount * cart.product.price
    # Create an OrderTableView object
    order_list.total = total
    order_list.save()
    order_table_view = OrderTableView.objects.create(
        customer_ID=request.user.customer,
        orderNumber=order_list,
        total=0,
        date=datetime.datetime.now()
    )
    order_table_view.save()

    pass


def profile_page(request):
    customer = Customer.objects.get(id_id=request.user.id)
    address = Address.objects.filter(customerId=customer).first()
    user = User.objects.get(id=customer.pk)
    return render(request, 'profileCustomer.html', {"customer": customer, "address": address, "user": user})


def orders_page(request):
    orders = OrdersList.objects.filter(customerID=request.user.customer)

    return render(request, 'ordersCustomer.html', {"orders": orders})


def addresses_page(request):
    addresses = Address.objects.filter(customerId=request.user.customer)

    return render(request, 'addressesCustomer.html', {"addresses": addresses})


def address_edit_page(request, id):
    address = Address.objects.get(id=id)

    return render(request, 'addressEditCustomer.html', {"address": address})


def address_update(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        country = request.POST.get('country')
        city = request.POST.get('city')
        district = request.POST.get('district')
        neighbourhood = request.POST.get('neighbourhood')
        streetName = request.POST.get('streetName')
        streetNo = request.POST.get('streetNumber')
        doorNo = request.POST.get('doorNumber')
        # Or if you are fetching customer by an ID from the form:
        # customer = Customer.objects.get(id=request.POST.get('customerId'))

        # Create new Address object
        address = Address.objects.get(id=id)
        address.title = title
        address.country = country
        address.city = city
        address.district = district
        address.neighbourhood = neighbourhood
        address.streetName = streetName
        address.streetNumber = streetNo
        address.doorNumber = doorNo
        address.save()
        return redirect("/addresses-page")


def address_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        country = request.POST.get('country')
        city = request.POST.get('city')
        district = request.POST.get('district')
        neighbourhood = request.POST.get('neighbourhood')
        streetName = request.POST.get('streetName')
        streetNo = request.POST.get('streetNumber')
        doorNo = request.POST.get('doorNumber')
        # Or if you are fetching customer by an ID from the form:
        # customer = Customer.objects.get(id=request.POST.get('customerId'))

        # Create new Address object
        address = Address.objects.create(
            customerId=request.user.customer,
            title=title,
            country=country,
            city=city,
            district=district,
            neighbourhood=neighbourhood,
            streetName=streetName,
            streetNumber=streetNo,
            doorNumber=doorNo,
        )

        return redirect("/addresses-page")

def order_details(request, order_id):
    orders = OrdersList.objects.get(orderNumber=order_id)
    virs = VirtualOrder.objects.filter(orderNumber=order_id)
    product_dict = {}
    rates = []
    for i in virs:
        if i.product.id in product_dict:
            # If product already exists in the dictionary, increment amount
            product_dict[i.product.id].product_amount += i.amount
        else:
            # If not, create a new Cart_details object and add to the dictionary
            obj = Cart_details()
            obj.product_id = i.product.id
            obj.product_name = i.product.product_name
            obj.product_price = i.product.price
            obj.product_amount = i.amount
            obj.total = obj.product_price * obj.product_amount
            obj.product_image = "/" + str(products_images.objects.filter(image_id=i.product).first().image)
            obj.rate = i.rating
            product_dict[i.product.id] = obj

    # Convert dictionary values to a list
    products1 = list(product_dict.values())
    return render(request, "order-detailsCustomer.html",
                  {"orders": orders, "products": products1, "total": (orders.total + 50)})


def profile_edit_page(request):
    customer = Customer.objects.get(id_id=request.user.id)
    address = Address.objects.get(customerId=customer)
    user = User.objects.get(id=customer.pk)

    return render(request, 'profileEditCustomer.html', {"customer": customer, "address": address, "user": user})


def profile_update(request):
    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        name = request.POST.get("name")
        customer = Customer.objects.get(id_id=request.user.id)
        user = User.objects.get(id=customer.pk)
        customer.customer_phone = phone
        customer.customer_name = name
        user.email = email
        customer.save()
        user.save()
    return redirect("/profile-page")


def review(request, id, order, star):
    product = Product.objects.get(id=id)
    order_number = OrdersList.objects.get(orderNumber=order)
    obj = VirtualOrder.objects.get(orderNumber=order_number, product=product)
    obj.rating = star
    obj.save()
    return redirect("/orders-details/" + str(order))

def address_add_page(request):
    return render(request, 'addressAddCustomer.html')

def remove_address(request,id):
    address=Address.objects.get(id=id)
    address.delete()
    return redirect("/addresses-page")
