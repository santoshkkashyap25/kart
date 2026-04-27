from django.test import TestCase
from app.models import Customer, Product, Cart, OrderPlaced
from django.contrib.auth.models import User

class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', locality='Test Locality', city='Test City', zipcode=123456, state='Test State')

    def test_customer_creation(self):
        self.assertIsInstance(self.customer, Customer)
        self.assertEqual(str(self.customer), f"{self.customer.name} ({self.customer.id})")

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(title='Test Product', selling_price=1000, discounted_price=800, description='Test Description', brand='Test Brand', category='M', product_image='test_product_image.jpg')

    def test_product_creation(self):
        self.assertIsInstance(self.product, Product)
        self.assertEqual(str(self.product), f"{self.product.title} ({self.product.id})")


class CartModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(title='Test Product', selling_price=1000, discounted_price=800, description='Test Description', brand='Test Brand', category='M', product_image='test_product_image.jpg')
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)

    def test_cart_creation(self):
        self.assertIsInstance(self.cart, Cart)
        self.assertEqual(str(self.cart), f"Cart: {self.user.username} - {self.product.title}")
        self.assertEqual(self.cart.total_cost, self.product.discounted_price * self.cart.quantity)


class OrderPlacedModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user, name='Test Customer', locality='Test Locality', city='Test City', zipcode=123456, state='Test State')
        self.product = Product.objects.create(title='Test Product', selling_price=1000, discounted_price=800, description='Test Description', brand='Test Brand', category='M', product_image='test_product_image.jpg')
        self.order_placed = OrderPlaced.objects.create(user=self.user, customer=self.customer, product=self.product, quantity=2, status='Pending')

    def test_order_placed_creation(self):
        self.assertIsInstance(self.order_placed, OrderPlaced)
        self.assertEqual(str(self.order_placed), f"Order {self.order_placed.id}: {self.user.username}")
        self.assertEqual(self.order_placed.total_cost, self.product.discounted_price * self.order_placed.quantity)
