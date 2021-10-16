from django.urls import path
from .views import *

app_name = "shopapp"

urlpatterns = [
    path('', home, name="home"),
    path('<slug:slug>', category, name="category"),
    path('<slug:slug>/<int:id>/', product_detail, name="product_detail"),
    path('cart_detail/', cart_detail, name="cart_detail"),
    path('checkout/', checkout, name='checkout'),
    path('ordering/', ordering, name='ordering'),
    path('order_end/', order_end, name='order_end'),
    path('profile/', profile, name='profile'),

    path('searching/', searching, name='searching'),

    path('sign_up/', sign_up, name="sign_up"),
    path('signin/', signin, name="signin"),
    path('logout/', logout, name="logout"),

    path('item_add/<int:id>', add_page, name='item_add'),
    path('item_increment/<int:id>', item_increment, name='item_increment'),
    path('item_decrement/<int:id>', item_decrement, name='item_decrement'),
    path('item_remove/<int:id>', remove, name='item_remove'),
    path('cart_clear/', cart_clear, name='cart_clear'),
]
