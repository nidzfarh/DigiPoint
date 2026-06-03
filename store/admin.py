from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('image',)

    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'brand',
        'is_active',
        'created_at'
    )

    list_filter = (
        'category',
        'is_active',
        'created_at'
    )

    search_fields = (
        'name',
        'brand',
        'description'
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('user__username',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'added_at')
    readonly_fields = ('added_at',)
    search_fields = ('product__name', 'cart__user__username')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'shipping_address')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    readonly_fields = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')