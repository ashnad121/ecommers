from django.shortcuts import render, get_object_or_404,redirect
from.models import Product,Cart
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


# Create your views here.

def home(request):
    # 1️⃣ Get category from URL
    category_name = request.GET.get('category')

    # 2️⃣ Filter products based on category
    if category_name:
       products = Product.objects.filter(category__category_name=category_name)
    else:
        products = Product.objects.all()

    # 3️⃣ Cart count
    cart_count = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            cart_count += item.quantity

    # 4️⃣ Context
    context = {
        'products': products,
        'cart_count': cart_count,
    }

    return render(request, 'index.html', context)
   

def category(request):
    return render(request,'categories.html')


@login_required
def single(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'single.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user, 
        product=product
        )

    if created:
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1

    # 👉 subtotal (total price)
    cart_item.total_price = cart_item.quantity * product.price

    cart_item.save()

    return redirect('cart_view')



@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = 0

    for items in cart_items:
        items.total_price = items.product.price * items.quantity 
        subtotal += items.total_price
    tax = subtotal * 0.1   # 10% tax
    total = subtotal + tax
    

    cart_count = 0
    for item in cart_items:
        cart_count += item.quantity 
        

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total,
        'cart_count': cart_count
        
    }
    return render(request, 'cart.html',context)


def increase_quantity(request, item_id):
    item = Cart.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_view')


def decrease_quantity(request, item_id):
    item =Cart.objects.get(id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()   

    return redirect('cart_view')

# remove cart

def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart, id=item_id)
    item.delete()
    return redirect('cart_view')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        return redirect('login')
    return render(request, 'register.html')
    

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_and_delete(request):
        logout(request)
        return redirect('register') 

def store(request):
    product = request.GET.get('product')

    if product:
        products = Product.objects.filter(
            product_name__icontains=product
        )
    else:
        products = Product.objects.all()

    return render(request, 'store.html', {'products': products})

