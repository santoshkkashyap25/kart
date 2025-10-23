from django.test import TestCase
from django.urls import reverse ,resolve
from app.views import *
from django.contrib.auth.views import * # to run some test cases present in forms not in views.py


class TestUrls(TestCase):
    
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, ProductView)

    def test_product_detail_url_resolves(self):
        url = reverse('product-detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, ProductDetailView)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add-to-cart')
        self.assertEqual(resolve(url).func, add_to_cart)

    def test_show_cart_url_resolves(self):
        url = reverse('showcart')
        self.assertEqual(resolve(url).func, show_cart)

    def test_plus_cart_url_resolves(self):
        url = reverse('plus_cart')
        self.assertEqual(resolve(url).func, plus_cart)

    def test_minus_cart_url_resolves(self):
        url = reverse('minus_cart')
        self.assertEqual(resolve(url).func, minus_cart)

    def test_remove_cart_url_resolves(self):
        url = reverse('remove_cart')
        self.assertEqual(resolve(url).func, remove_cart)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_address_url_resolves(self):
        url = reverse('address')
        self.assertEqual(resolve(url).func, address)

    def test_orders_url_resolves(self):
        url = reverse('orders')
        self.assertEqual(resolve(url).func, orders)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, checkout)

    def test_paymentdone_url_resolves(self):
        url = reverse('paymentdone')
        self.assertEqual(resolve(url).func, payment_done)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_passwordchange_url_resolves(self):
        url = reverse('passwordchange')
        self.assertEqual(resolve(url).func.view_class, PasswordChangeView)

    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, PasswordResetCompleteView)

    def test_customer_registration_url_resolves(self):
        url = reverse('customerregistration')
        self.assertEqual(resolve(url).func.view_class, CustomerRegistrationView)


    # Wishlist URLs
    def test_show_wishlist_url_resolves(self):
        url = reverse('wishlist')
        self.assertEqual(resolve(url).func, show_wishlist)

    def test_add_to_wishlist_url_resolves(self):
        url = reverse('add_to_wishlist')
        self.assertEqual(resolve(url).func, add_to_wishlist)

    def test_remove_from_wishlist_url_resolves(self):
        url = reverse('remove_from_wishlist')
        self.assertEqual(resolve(url).func, remove_from_wishlist)

    # Review URLs
    def test_add_review_url_resolves(self):
        url = reverse('add_review', args=[1])
        self.assertEqual(resolve(url).func, add_review)

    # Search URLs
    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, ProductSearchView)

    # Export Orders
    def test_export_orders_url_resolves(self):
        url = reverse('export_orders')
        self.assertEqual(resolve(url).func, export_order_history)

    # Recently Viewed
    def test_recently_viewed_url_resolves(self):
        url = reverse('recently_viewed')
        self.assertEqual(resolve(url).func, show_recently_viewed)

    # Track and Cancel Orders
    def test_track_order_url_resolves(self):
        url = reverse('track_order', args=[1])
        self.assertEqual(resolve(url).func, track_order)

    def test_cancel_order_url_resolves(self):
        url = reverse('cancel_order', args=[1])
        self.assertEqual(resolve(url).func, cancel_order)

    # Product Quick View
    def test_product_quick_view_url_resolves(self):
        url = reverse('product_quick_view', args=[1])
        self.assertEqual(resolve(url).func, product_quick_view)

    # Category and Filter URLs
    def test_category_url_resolves(self):
        url = reverse('category', args=['laptop'])
        self.assertEqual(resolve(url).func, category_view)

    def test_category_filter_url_resolves(self):
        url = reverse('category_filter', args=['laptop', 'brand'])
        self.assertEqual(resolve(url).func, category_view)




