from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    logo = models.ImageField(upload_to="media")
    company_name = models.CharField(max_length=30)
    type = models.CharField(max_length=20)
    tax_no = models.IntegerField()
    created_date = models.DateField(auto_now_add=True, null=True)
    is_activated = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        db_table = 'company'


class Company_User(models.Model):
    company = models.OneToOneField(Company, models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    price = models.FloatField()
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    amount = models.IntegerField()
    is_available = models.BooleanField()
    category = models.CharField(max_length=15)

    class Meta:
        db_table = 'product'


class ProductSize(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=200)
    amount = models.IntegerField()

    class Meta:
        db_table = 'product_sizes'

    def save(self, *args, **kwargs):
        # Get the previous value if the object already exists
        if self.pk:
            previous = ProductSize.objects.get(pk=self.pk)
            diff = previous.amount - self.amount
            self.product.amount -= diff
            self.product.save()
        super(ProductSize, self).save(*args, **kwargs)


class products_images(models.Model):
    image_id = models.OneToOneField(Product, models.CASCADE, unique=False, primary_key=False)
    image = models.ImageField()
    color = models.CharField(max_length=10)


class Tokens(models.Model):
    id = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=200)
    date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'tokens'


class Customer(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    customer_name = models.CharField(max_length=200)
    customer_TC = models.IntegerField()
    customer_birthdate = models.DateField()
    customer_gender = models.BooleanField()
    customer_phone = models.IntegerField()


class Address(models.Model):
    customerId = models.OneToOneField(Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    neighbourhood = models.CharField(max_length=100)
    streetName = models.CharField(max_length=100)
    streetNumber = models.CharField(max_length=100)
    doorNumber = models.CharField(max_length=100)


class OrdersList(models.Model):
    orderNumber = models.IntegerField(primary_key=True, auto_created=True)
    status = models.BooleanField()
    date = models.DateField()
    customerID = models.OneToOneField(Customer, on_delete=models.CASCADE)
    total = models.FloatField()
    date = models.DateField(auto_now=True)


class VirtualOrder(models.Model):
    orderNumber = models.OneToOneField(OrdersList, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    rating = models.IntegerField()


class OrderTableView(models.Model):
    customer_ID = models.OneToOneField(Customer, on_delete=models.CASCADE)
    orderNumber = models.OneToOneField(OrdersList, on_delete=models.CASCADE)
    total = models.FloatField()
    date = models.DateField()


class Company_orders_list(models.Model):
    orderNumber = models.IntegerField(primary_key=True)
    products = models.OneToOneField(VirtualOrder, on_delete=models.CASCADE)
    datetime = models.DateField()


class Company_VirtualOrder(models.Model):
    orderNumber = models.OneToOneField(OrdersList, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Invoice(models.Model):
    companyID = models.OneToOneField(Company, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    total = models.FloatField()
    products = models.OneToOneField(Company_orders_list, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    datetime = models.DateField()


class AdminSales(models.Model):
    date = models.DateField()
    total = models.FloatField()


class AdminProfit(models.Model):
    date = models.DateField()
    total = models.FloatField()


class Cart(models.Model):
    product_sizes = models.OneToOneField(ProductSize, models.CASCADE)
    product = models.OneToOneField(Product, models.CASCADE)
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        db_table = 'cart'


class GenderProducts(models.Model):
    product = models.OneToOneField(Product, models.CASCADE)
    gender = models.BooleanField()
