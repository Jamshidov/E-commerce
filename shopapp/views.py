from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from .models import *
from .forms import *
from .cart import Cart


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    page = request.GET.get('page')
    pg = Paginator(products, 2)

    try:
        pages = pg.page(page)
    except PageNotAnInteger:
        pages = pg.page(1)
    except EmptyPage:
        pages = pg.page(pg.num_pages)

    context = {
        "products": products,
        "categories": categories,
        "pages": pages,
    }
    return render(request, 'shopapp/params/index.html', context)


def category(request, slug):
    products = Product.objects.filter(category__slug=slug)
    categories = Category.objects.all()

    pg = Paginator(products, 2)
    page = request.GET.get('page')

    try:
        products = pg.page(page)
    except PageNotAnInteger:
        products = pg.page(1)
    except EmptyPage:
        products = pg.page(pg.num_pages)

    context = {
        "products": products,
        "pages": products,
        "categories": categories,
        "pg": pg,
    }
    return render(request, 'shopapp/params/index.html', context)


def searching(request):
    if request.method == "GET":
        search_item = request.GET['q'].title().strip()
        products = Product.objects.filter(Q(name__icontains=search_item) | Q(title__icontains=search_item))

        pagination = Paginator(products, 2)
        page = request.GET.get('page')

        try:
            products = pagination.page(page)
        except PageNotAnInteger:
            products = pagination.page(1)
        except EmptyPage:
            products = pagination.page(pagination.num_pages)

        context = {
            "products": products,
            "pages": products,
        }

        return render(request, 'shopapp/params/index.html', context)
    else:
        return redirect("home")


def product_detail(request, slug, id):
    product = Product.objects.filter(category__slug=slug, id=id)
    context = {"product": product}
    return render(request, 'shopapp/params/product_detail.html', context)


def add_page(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("shopapp:home")


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("shopapp:cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("shopapp:cart_detail")


def remove(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("shopapp:cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("shopapp:home")


def cart_detail(request):
    cart = Cart(request)
    items = cart.items()
    total_price = cart.get_total_price()
    count = cart.get_total_items()

    context = {
        "items": items,
        "count": count,
        "total_price": total_price,
    }
    return render(request, 'shopapp/params/cart_detail.html', context)


def checkout(request):
    if 'customer' in request.session:
        mylogin = request.session['customer']['username']
        username = mylogin
        user_obj = Customer.objects.get(username=username)

        if 'cart' in request.session:

            cart = Cart(request)
            items = cart.items()
            total_price = cart.get_total_price()

            context = {
                "items": items,
                "total_price": total_price,
                "user_obj": user_obj,
            }

        else:
            context = {}

    else:
        context = {}

    return render(request, 'shopapp/params/order.html', context)


def sign_up(request):
    if request.method == "GET":
        return render(request, 'shopapp/params/sign_up.html')
    elif request.method == "POST":
        userData = request.POST
        username = userData['username']
        email = userData['email']
        password1 = userData['password1']
        password2 = userData['password2']
        first_name = userData['first_name']
        last_name = userData['last_name']
        phone = userData['phone']
        address = userData['address']

        if password1 == password2:
            if Customer.objects.filter(username=username).exists():
                messages.error(request, "The Username Already Exists")
                return redirect('shopapp:sign_up')
            elif Customer.objects.filter(email=email).exists():
                messages.error(request, "The Email Already Exists")
                return redirect('shopapp:sign_up')
            else:
                customer = Customer.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    address=address,
                    password=password1,

                )
                customer.save()
                return redirect('shopapp:signin')
        else:
            messages.error(request, "password no match")
            return redirect('shopapp:sign_up')
    else:
        pass


def signin(request):
    user_account = False
    if request.method == "GET":
        return render(request, 'shopapp/params/signin.html')
    elif request.method == "POST":
        userData = request.POST
        username = userData['username']
        password = userData['password']

        if not username or not password:
            messages.error(request, "Please enter your registered data")
            return redirect("shopapp:signin")
        else:
            # loginData = Customer.objects.filter(username=username, password=password)
            loginData = Customer.userExists(username=username)
            if loginData:
                if password == loginData.password:
                    request.session['customer'] = {'id': loginData.id, 'username': loginData.username}
                    request.session.modified = True
                    user_account = True
                    return redirect('shopapp:home')
                else:
                    messages.error(request, "Password None")
                    return redirect('shopapp:signin')
            else:
                messages.error(request, "User None")
                return redirect('shopapp:signin')

    else:
        pass


def logout(request):
    request.session.clear()
    user_account = False
    return redirect('shopapp:signin')

# =========================================

def ordering(request):
    cart_end = Cart(request)
    cart = request.session['cart']
    if request.method == "POST":
        form = OrderForms(request.POST)
        if form.is_valid():
            order = form.save()
            for items in cart.values():
                OrderItem.objects.create(
                    order=order,
                    product=items['name'],
                    price=items['price'],
                    quantity=items['quantity'],
                    total_price=items['quantity']*int(items['price'])
                )
                # print(items['quantity'] * int(items['price']))
            cart_end.clear()
            return redirect("shopapp:order_end")
        else:
            messages.error(request, "invalid form")
    else:
        return redirect("shopapp:checkout")


def order_end(request):
    username = request.session['customer']['username']
    # print(username)
    orders = Order.objects.filter(customer=username)

    items = []
    for item in orders:
        items.append(item)
    context = {
        "items": items,
        "orders": orders,
    }

    return render(request, 'shopapp/params/end.html', context)


def profile(request):
    username = request.session['customer']['username']

    items = Customer.objects.filter(username=username)
    orders = Order.objects.filter(customer=username)

    context = {
        "username": username,
        "orders": orders,
        "items": items,
    }

    return render(request, 'shopapp/params/profile.html', context)