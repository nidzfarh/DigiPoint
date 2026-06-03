from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from decimal import Decimal
from django.contrib.auth.models import User
from .models import Order
from .forms import ProductForm
from .models import Product, Cart, CartItem, Order, OrderItem
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, OrderForm,
    ProductSearchForm, CartQuantityForm
)


# auth
def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('store:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create cart for new user
            Cart.objects.create(user=user)
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            
            messages.success(request, 'Account created successfully! Welcome to DigiPoint.')
            return redirect('store:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'store/auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('store:home')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'store/auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('store:home')


#product
def home_view(request):
    """Home page with featured products."""
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    featured_products = products[:4]
    
    context = {
        'featured_products': featured_products,
        'total_products': Product.objects.filter(is_active=True).count(),
    }
    context.update({
        'total_users': User.objects.count(),
        'total_orders': Order.objects.count(),
    })
    return render(request, 'store/home.html', context)


def products_list_view(request):
    products = Product.objects.filter(is_active=True)
    form = ProductSearchForm(request.GET or None)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) |Q(description__icontains=search_query) |Q(brand__icontains=search_query))
    
    # Category filter
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['-created_at', 'price', '-price', 'name']:
        products = products.order_by(sort_by)
    
    context = {'products': products,'form': form,'search_query': search_query,'selected_category': category,}
    return render(request, 'store/products.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(pk=pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


#cart
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required(login_url='store:login')
def cart_view(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='store:login')
def add_to_cart_view(request, product_id):
    if request.method != 'POST':
        return redirect('store:product_detail', pk=product_id)
    
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request.user)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity value.')
        return redirect('store:product_detail', pk=product_id)
    
    if quantity < 1:
        quantity = 1
    
    if quantity > product.stock:
        messages.error(request, f'Only {product.stock} items available in stock.')
        return redirect('store:product_detail', pk=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart,product=product,defaults={'quantity': quantity})
    
    if not created:
        new_quantity = cart_item.quantity + quantity
        if new_quantity > product.stock:
            messages.error(request, f'Only {product.stock} items available in stock.')
            return redirect('store:cart')
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity in cart.')
    else:
        messages.success(request, f'Added {product.name} to cart.')
    
    return redirect('store:cart')


@login_required(login_url='store:login')
def remove_from_cart_view(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed {product_name} from cart.')
    return redirect('store:cart')


@login_required(login_url='store:login')
def update_cart_item_view(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        form = CartQuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            if quantity > cart_item.product.stock:
                messages.error(request, f'Only {cart_item.product.stock} items available.')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, f'Updated quantity.')
    
    return redirect('store:cart')
# checkout
@login_required(login_url='store:login')
def checkout_view(request):
    cart = get_or_create_cart(request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('store:cart')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                # Update product stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully! Thank you for your purchase.')
            return redirect('store:order_confirmation', pk=order.pk)
    else:
        form = OrderForm()
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'store/checkout.html', context)


@login_required(login_url='store:login')
def order_confirmation_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'store/order_confirmation.html', context)


@login_required(login_url='store:login')
def order_history_view(request):
    orders = request.user.orders.all()
    
    context = {
        'orders': orders,
    }
    return render(request, 'store/order_history.html', context)


@login_required(login_url='store:login')
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order_items = order.items.all()
    
    context = {'order': order,'order_items': order_items,}
    return render(request, 'store/order_detail.html', context)


#admin views
@login_required(login_url='store:login')
def admin_dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('store:home')
    
    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'total_users': User.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'recent_orders': Order.objects.all()[:5],
    }
    return render(request, 'store/admin/dashboard.html', context)


@login_required(login_url='store:login')
def admin_products_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('store:home')
    
    products = Product.objects.all()
    
    context = {
        'products': products,
    }
    return render(request, 'store/admin/products.html', context)
@login_required(login_url='store:login')
def add_product_view(request):
    if not request.user.is_staff:
        return redirect('store:home')

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('store:admin_products')
    else:
        form = ProductForm()

    return render(request, 'store/admin/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })


@login_required(login_url='store:login')
def edit_product_view(request, pk):
    if not request.user.is_staff:
        return redirect('store:home')

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('store:admin_products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/admin/product_form.html', {
        'form': form,
        'title': 'Edit Product'
    })


@login_required(login_url='store:login')
def delete_product_view(request, pk):
    if not request.user.is_staff:
        return redirect('store:home')

    product = get_object_or_404(Product, pk=pk)

    product.delete()

    messages.success(request, 'Product deleted successfully.')

    return redirect('store:admin_products')

@login_required(login_url='store:login')
def admin_orders_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('store:home')
    
    orders = Order.objects.all()
    
    context = {'orders': orders,}
    return render(request, 'store/admin/orders.html', context)

# util
def about_view(request):
    return render(request, 'store/about.html')


def contact_view(request):
    return render(request, 'store/contact.html')
