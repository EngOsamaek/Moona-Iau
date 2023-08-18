from django.test import TestCase
from .models import Company, Product, Customer, Address
from django.contrib.auth.models import User


class CompanyModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            logo="path/to/logo",
            company_name="Test Company",
            type="Test Type",
            tax_no=12345678,
            is_activated=True,
            is_blocked=False,
        )

    def test_company_creation(self):
        self.assertTrue(isinstance(self.company, Company))
        self.assertEqual(self.company.__str__(), self.company.company_name)


class ProductModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            logo="path/to/logo",
            company_name="Test Company",
            type="Test Type",
            tax_no=12345678,
            is_activated=True,
            is_blocked=False,
        )

        self.product = Product.objects.create(
            product_name="Test Product",
            price=100.0,
            company=self.company,
            amount=50,
            is_available=True,
            category="Test Category",
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(self.product.__str__(), self.product.product_name)


class CustomerModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.customer = Customer.objects.create(
            id=self.user,
            customer_name="Test Customer",
            customer_TC=12345678901,
            customer_birthdate="1990-01-01",
            customer_gender=True,
            customer_phone=1234567890,
        )

    def test_customer_creation(self):
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(self.customer.__str__(), self.customer.customer_name)


class AddressModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

        self.customer = Customer.objects.create(
            id=self.user,
            customer_name="Test Customer",
            customer_TC=12345678901,
            customer_birthdate="1990-01-01",
            customer_gender=True,
            customer_phone=1234567890,
        )

        self.address = Address.objects.create(
            customerId=self.customer,
            country="Test Country",
            city="Test City",
            district="Test District",
            neighbourhood="Test Neighbourhood",
            streetName="Test Street",
            streetNumber=10,
            doorNumber=1,
        )

    def test_address_creation(self):
        self.assertTrue(isinstance(self.address, Address))
        self.assertEqual(self.address.__str__(), self.address.streetName)
