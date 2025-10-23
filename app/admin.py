"""
Enhanced Admin Panel with Advanced Features
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.utils.html import format_html

# Inline Admin Classes
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary']

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created_at']
    can_delete = True

# Enhanced Customer Admin
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'city', 'state', 'total_orders', 'total_spent']
    list_filter = ['state', 'city']
    search_fields = ['name', 'user__username', 'user__email', 'locality']
    readonly_fields = ['total_orders', 'total_spent']
    
    def total_orders(self, obj):
        count = OrderPlaced.objects.filter(customer=obj).count()
        return count
    total_orders.short_description = 'Total Orders'
    
    def total_spent(self, obj):
        total = sum(order.total_cost for order in OrderPlaced.objects.filter(customer=obj))
        return f'₹{total:.2f}'
    total_spent.short_description = 'Total Spent'


# Enhanced Product Admin
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'brand', 'category', 'selling_price', 
        'discounted_price', 'discount_percentage',
        'stock_status',
        'average_rating_display', 'total_orders', 'is_featured'
    ]

    list_filter = ['category', 'brand', 'is_featured', 'is_bestseller', 'is_new_arrival']
    search_fields = ['title', 'brand', 'description']
    list_editable = ['is_featured', 'selling_price', 'discounted_price']
    inlines = [ProductImageInline, ReviewInline]
    actions = ['make_featured', 'make_bestseller', 'apply_discount', 'mark_out_of_stock']

    readonly_fields = ['average_rating_display', 'total_orders', 'created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {'fields': ('title', 'brand', 'category', 'description')}),
        ('Pricing', {'fields': ('selling_price', 'discounted_price', 'sku')}),
        ('Inventory', {'fields': ('stock_quantity', 'weight')}),
        ('Marketing', {'fields': ('is_featured', 'is_bestseller', 'is_new_arrival')}),
        ('Media', {'fields': ('product_image',)}),
        ('Statistics', {'fields': ('average_rating_display', 'total_orders', 'sold_count', 'created_at', 'updated_at'),
                        'classes': ('collapse',)}),
    )

    def discount_percentage(self, obj):
        if obj.selling_price > 0:
            discount = ((obj.selling_price - obj.discounted_price) / obj.selling_price) * 100
            return format_html('<span style="color: green; font-weight: bold;">{}%</span>', round(discount, 1))
        return '0%'
    discount_percentage.short_description = 'Discount'


    # Stock display
    def stock_status(self, obj):
        if obj.stock_quantity > 20:
            color = 'green'
            status = f'In Stock ({obj.stock_quantity})'
        elif obj.stock_quantity > 0:
            color = 'orange'
            status = f'Low Stock ({obj.stock_quantity})'
        else:
            color = 'red'
            status = 'Out of Stock'
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, status)
    stock_status.short_description = 'Stock'

    def average_rating_display(self, obj):
        avg = obj.average_rating or 0
        stars = '⭐' * int(avg)
        formatted_avg = f'{avg:.1f}' 
        return format_html('{} ({})', stars, formatted_avg)
    average_rating_display.short_description = 'Rating'


    # Total orders
    def total_orders(self, obj):
        return OrderPlaced.objects.filter(product=obj).count()
    total_orders.short_description = 'Orders'

    # Admin actions
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} products marked as featured')
    make_featured.short_description = 'Mark as Featured'

    def make_bestseller(self, request, queryset):
        queryset.update(is_bestseller=True)
        self.message_user(request, f'{queryset.count()} products marked as bestseller')
    make_bestseller.short_description = 'Mark as Bestseller'


    def apply_discount(self, request, queryset):
        for product in queryset:
            product.discounted_price = product.selling_price * 0.9
            product.save()
        self.message_user(request, f'10% discount applied to {queryset.count()} products')
    apply_discount.short_description = 'Apply 10%% Discount' 


    def mark_out_of_stock(self, request, queryset):
        queryset.update(stock_quantity=0)
        self.message_user(request, f'{queryset.count()} products marked out of stock')
    mark_out_of_stock.short_description = 'Mark Out of Stock'

# Enhanced Cart Admin
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_cost']
    list_filter = ['user']
    search_fields = ['user__username', 'product__title']
    
    def total_cost(self, obj):
        return f'₹{obj.total_cost:.2f}'
    total_cost.short_description = 'Total Cost'

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    # Only include the actual model field `status` in list_editable
    list_display = [
        'id', 'order_date', 'user_link', 'customer_link', 
        'product_link', 'quantity', 'total_cost_display', 'status', 'payment_status'
    ]
    list_editable = ['status']  # keep only model field

    list_filter = ['status', 'ordered_date', 'customer__state']
    search_fields = ['user__username', 'customer__name', 'product__title']
    readonly_fields = ['ordered_date', 'total_cost_display']
    date_hierarchy = 'ordered_date'
    actions = ['mark_as_delivered', 'mark_as_cancelled', 'export_to_csv']

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'customer', 'product', 'quantity', 'ordered_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Cost', {
            'fields': ('total_cost_display',),
            'classes': ('collapse',)
        }),
    )

    def order_date(self, obj):
        return obj.ordered_date.strftime('%Y-%m-%d %H:%M')
    order_date.short_description = 'Order Date'

    def user_link(self, obj):
        link = reverse("admin:auth_user_change", args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', link, obj.user.username)
    user_link.short_description = 'User'

    def customer_link(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    customer_link.short_description = 'Customer'

    def product_link(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    product_link.short_description = 'Product'

    def total_cost_display(self, obj):
        formatted_total = f"{obj.total_cost:.2f}"
        return format_html('₹{}', formatted_total)


    def payment_status(self, obj):
        if obj.status == 'Delivered':
            return format_html('<span style="color: green;">✓ Paid</span>')
        return format_html('<span style="color: orange;">⏳ Pending</span>')
    payment_status.short_description = 'Payment'

    # Admin Actions
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')
        self.message_user(request, f'{queryset.count()} orders marked as delivered')
    mark_as_delivered.short_description = 'Mark as Delivered'

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='Cancel')
        self.message_user(request, f'{queryset.count()} orders cancelled')
    mark_as_cancelled.short_description = 'Cancel Orders'

    def export_to_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'

        writer = csv.writer(response)
        writer.writerow(['Order ID', 'User', 'Customer', 'Product', 'Quantity', 'Total', 'Status', 'Date'])

        for order in queryset:
            writer.writerow([
                order.id,
                order.user.username,
                order.customer.name,
                order.product.title,
                order.quantity,
                order.total_cost,
                order.status,
                order.ordered_date.strftime('%Y-%m-%d')
            ])

        return response
    export_to_csv.short_description = 'Export to CSV'


# Wishlist Admin
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__title']
    date_hierarchy = 'added_at'


# Review Admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'rating_display', 'verified_purchase', 'created_at']
    list_filter = ['rating', 'verified_purchase', 'created_at']
    search_fields = ['user__username', 'product__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['verify_purchases', 'mark_helpful']
    
    def rating_display(self, obj):
        stars = '⭐' * obj.rating
        return format_html('{} ({})', stars, obj.rating)
    rating_display.short_description = 'Rating'
    
    def verify_purchases(self, request, queryset):
        queryset.update(verified_purchase=True)
        self.message_user(request, f'{queryset.count()} reviews marked as verified')
    verify_purchases.short_description = 'Mark as Verified Purchase'
    
    def mark_helpful(self, request, queryset):
        for review in queryset:
            review.helpful_count += 1
            review.save()
        self.message_user(request, f'{queryset.count()} reviews marked as helpful')
    mark_helpful.short_description = 'Increase Helpful Count'


# User Profile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'email_verified', 'newsletter_subscribed', 'created_at']
    list_filter = ['email_verified', 'newsletter_subscribed', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']


# Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'created_at', 'is_read', 'replied']
    list_filter = ['is_read', 'replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} messages marked as read')
    mark_as_read.short_description = 'Mark as Read'
    
    def mark_as_replied(self, request, queryset):
        queryset.update(replied=True)
        self.message_user(request, f'{queryset.count()} messages marked as replied')
    mark_as_replied.short_description = 'Mark as Replied'


# Flash Sale Admin
# @admin.register(FlashSale)
# class FlashSaleAdmin(admin.ModelAdmin):
#     list_display = ['product', 'sale_price', 'start_time', 'end_time', 'is_active', 'sales_progress']
#     list_filter = ['is_active', 'start_time', 'end_time']
#     search_fields = ['product__title']
#     list_editable = ['is_active']
    
#     def sales_progress(self, obj):
#         percentage = (obj.sold_quantity / obj.max_quantity) * 100 if obj.max_quantity > 0 else 0
#         return format_html(
#             '<progress value="{}" max="100" style="width: 100px;"></progress> {}%',
#             percentage, round(percentage, 1)
#         )
#     sales_progress.short_description = 'Sales Progress'


# Banner Admin
# @admin.register(Banner)
# class BannerAdmin(admin.ModelAdmin):
#     list_display = ['title', 'subtitle', 'is_active', 'display_order']
#     list_filter = ['is_active']
#     search_fields = ['title', 'subtitle']
#     list_editable = ['is_active', 'display_order']


# User Notification Admin
@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} notifications marked as read')
    mark_as_read.short_description = 'Mark as Read'



# Customize Admin Site
admin.site.site_header = "KART Admin Dashboard"
admin.site.site_title = "KART Admin"
admin.site.index_title = "Welcome to KART Administration"