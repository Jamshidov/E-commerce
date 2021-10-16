from django.db import models
from django.urls import reverse


class Customer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    phone = models.PositiveBigIntegerField()
    address = models.TextField()
    password = models.CharField(max_length=100)
    objects = models.Manager()

    class Meta:
        verbose_name = "Клиента"
        verbose_name_plural = "1. Клиенты"

    def __str__(self):
        return self.username

    @staticmethod
    def userExists(username):
        try:
            username = Customer.objects.get(username=username)
            return username
        except:
            return False


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Категорию"
        verbose_name_plural = "2. Категории"

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('shopapp:category', args=[self.slug])


class Product(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Categories")
    image = models.ImageField(upload_to='images/products')
    price = models.PositiveIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "3. Товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shopapp:product_detail', args=[self.category, self.id])


class Order(models.Model):
    customer = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveBigIntegerField()
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    confirmation = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = '4. Заказы'

    def __str__(self):
        return '{}'.format(self.id)

    def confirm(self):
        return self.confirmation

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())

    def customer_order(self):
        a = [item.ordering() for item in self.items.all()]
        return a


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()
    objects = models.Manager()

    def __str__(self):
        return '{}'.format(self.id)

    def ordering(self):
        return '{} - x{} - {} сум'.format(self.product, self.quantity, self.total_price)

