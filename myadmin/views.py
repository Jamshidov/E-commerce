from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import ProductForm
from shopapp.models import Order, OrderItem


@login_required(login_url="myadmin:login_page")
def index(request):
    order1 = Order.objects.all()
    order2 = OrderItem.objects.all()

    context = {
        "order1": order1,
        "order2": order2,
    }
    return render(request, 'myadmin/dirs/index.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("myadmin:myadmin")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("myadmin:myadmin")
            else:
                messages.error(request, "User none")
        else:
            pass

        return render(request, 'myadmin/dirs/login.html')


def logout_page(request):
    logout(request)
    return redirect("myadmin:login_page")


def product_create(request):
    form = ProductForm
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("myadmin:myadmin")
        else:
            messages.error(request, "error")

    context = {
        "form": form,
    }

    return render(request, 'myadmin/dirs/product_add.html', context)

