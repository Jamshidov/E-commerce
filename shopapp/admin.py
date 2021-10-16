from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'name', 'category', 'price', 'created')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name', )}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'first_name', 'last_name', 'email', 'phone', 'created']
    list_display_links = ['id', 'customer', 'first_name']
    search_fields = ['id', 'customer', 'first_name', 'last_name', 'email', 'phone']
    inlines = [OrderItemInline]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)


