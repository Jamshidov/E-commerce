# Generated by Django 3.2.7 on 2021-10-14 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Категорию',
                'verbose_name_plural': '2. Категории',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=30)),
                ('phone', models.PositiveBigIntegerField()),
                ('address', models.TextField()),
                ('password', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Клиента',
                'verbose_name_plural': '1. Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveBigIntegerField()),
                ('address', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('confirmation', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': '4. Заказы',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/products')),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Categories', to='shopapp.category')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': '3. Товары',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_price', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shopapp.order')),
            ],
        ),
    ]
