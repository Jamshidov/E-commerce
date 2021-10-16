from django.urls import path
from . import views

app_name = "myadmin"

urlpatterns = [
    path('', views.index, name="myadmin"),
    path('product_add/', views.product_create, name="add_product"),
    path('login/', views.login_page, name="login_page"),
    path('logout/', views.logout_page, name="logout_page"),
]



