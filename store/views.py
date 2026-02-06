from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Product, Order, Category

from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
# --- USER CODE (Registration) ---
def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# --- USER LOGOUT ---
def request_otp(request):
    """View to request an OTP to be sent to the provided email."""
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, 'Please provide an email address.')
            return redirect('request_otp')

        otp = str(random.randint(100000, 999999))
        expiry_ts = (timezone.now() + timedelta(minutes=10)).timestamp()

        # Store OTP details in session
        request.session['otp'] = otp
        request.session['otp_email'] = email
        request.session['otp_expiry'] = expiry_ts

        subject = 'Your login OTP'
        message = f'Your OTP is {otp}. It will expire in 10 minutes.'
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', settings.EMAIL_HOST_USER)
        try:
            send_mail(subject, message, from_email, [email])
            messages.success(request, f'An OTP has been sent to {email}.')
        except Exception as e:
            messages.error(request, f'Failed to send OTP: {e}')
            return redirect('request_otp')

        return redirect('verify_otp')

    return render(request, 'otp_request.html')


def verify_otp(request):
    """View to verify the OTP entered by the user and log them in."""
    if request.method == 'POST':
        entered = request.POST.get('otp')
        session_otp = request.session.get('otp')
        expiry_ts = request.session.get('otp_expiry')
        email = request.session.get('otp_email')

        if not session_otp or not expiry_ts or not email:
            messages.error(request, 'No OTP request found. Please request a new OTP.')
            return redirect('request_otp')

        if timezone.now().timestamp() > float(expiry_ts):
            messages.error(request, 'OTP has expired. Please request a new one.')
            return redirect('request_otp')

        if entered == session_otp:
            user, created = User.objects.get_or_create(username=email, defaults={'email': email})
            if created:
                user.set_unusable_password()
                user.save()

            login(request, user)

            # Clear OTP from session
            for k in ('otp', 'otp_email', 'otp_expiry'):
                request.session.pop(k, None)

            return redirect('home')

        messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'otp_verify.html')
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return render(request, 'logout_success.html')

# --- PRODUCT DETAIL ---
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# --- PROFILE ---
@login_required(login_url='login')
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': orders})

# --- CHECKOUT CODE ---
@login_required(login_url='register') # Redirects to register if not logged in
def checkout(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'main/checkout.html', {'product': product})

# --- PAYMENT CODE ---
@login_required(login_url='register')
def payment(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        # Create order after payment
        order = Order.objects.create(
            user=request.user,
            total_price=product.price,
            complete=True
        )
        return redirect('order_success')
    return render(request, 'main/payment.html', {'product': product})

# --- ORDER SUCCESS ---
@login_required(login_url='register')
def order_success(request):
    return render(request, 'main/order_success.html')

# --- MY ORDERS CODE ---
@login_required(login_url='register')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

# --- ADMIN SALES REPORT ---
def sales_report(request):
    if not request.user.is_staff: # Only admins can see this
        return redirect('home')
    total_sales = Order.objects.filter(complete=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/sales_report.html', {'total_sales': total_sales, 'orders': orders})

def home(request):
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()
    new_products = Product.objects.filter(is_new=True)[:6]
    
    return render(request, 'home.html', {
        'products': products, 
        'categories': categories,
        'new_products': new_products,
        'selected_category': category_id
    })