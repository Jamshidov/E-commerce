from django.forms import ModelForm
from .models import Order


class OrderForms(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'first_name', 'last_name', 'email', 'phone', 'address']