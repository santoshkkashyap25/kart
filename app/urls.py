from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app import views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    # Home
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    # Cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='remove_cart'),

    # Wishlist
    path('wishlist/', views.show_wishlist, name='wishlist'),
    path('add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Reviews
    path('add-review/<int:pk>/', views.add_review, name='add_review'),

    # Search
    path('search/', views.ProductSearchView.as_view(), name='search'),

    # Profile & Address
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),

    # Orders
    path('orders/', views.orders, name='orders'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('export-orders/', views.export_order_history, name='export_orders'),

    # Recently Viewed
    path('recently-viewed/', views.show_recently_viewed, name='recently_viewed'),

    # Checkout & Payment
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    # AJAX Quick View
    path('product-quick-view/<int:pk>/', views.product_quick_view, name='product_quick_view'),

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='app/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Password Management
    path('passwordchange/', auth_views.PasswordChangeView.as_view(
        template_name='app/passwordchange.html',
        form_class=MyPasswordChangeForm,
        success_url='/passwordchangedone/'
    ), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'
    ), name='passwordchangedone'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='app/password_reset.html',
        form_class=MyPasswordResetForm
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=MySetPasswordForm
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('<str:category>/<slug:filter_type>/', views.category_view, name='category_filter'),
    path('<str:category>/', views.category_view, name='category'),
]

# Serve media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
