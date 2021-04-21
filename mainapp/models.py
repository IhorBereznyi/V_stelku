from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Найменування')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Зображення')
    code = models.CharField(max_length=234, verbose_name='Код продукту', blank=True)
    description = models.TextField(verbose_name='Опис', null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=0, verbose_name='Стара ціна')
    sale = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Знижка', blank=True)
    size = models.CharField(max_length=255, verbose_name='Розмір')
    material = models.CharField(max_length=255, verbose_name='Матеріал', blank=True)
    color = models.CharField(max_length=255, verbose_name='Колір', blank=True)
    inside = models.CharField(max_length=255, verbose_name='Всередині', blank=True)
    sole = models.CharField(max_length=255, verbose_name='Підошва', blank=True)
    features = models.ManyToManyField("specs.ProductFeatures", blank=True, related_name='features_for_product')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_features(self):
        return {f.feature.feature_name: ' '.join([f.value, f.feature.unit or ""]) for f in self.features.all()}

    def get_sale(self): # Розрахувати вартість знижки
        price = int(self.price * (100 - self.sale) / 100)
        return price



class Image(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, default=None, related_name='images', on_delete=models.PROTECT)


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Загальна ціна')

    def __str__(self):
        return "Продукт: {} (для корзини)".format(self.product.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.get_sale()
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Загальна цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Замовлення покупця', related_name='related_order')

    def __str__(self):
        return "Покупець: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в обробці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконане')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Нова пошта'),
        (BUYING_TYPE_DELIVERY, 'Укрпошта')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупець', related_name='related_orders',
                                 on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Імя')
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1424, verbose_name='Адрес доставки', null=True)
    num_vid = models.CharField(max_length=200, verbose_name='Номер відділення', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Доставка',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Коментар до замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')
    order_date = models.DateField(verbose_name='Дата отримки замовлення', default=timezone.now)

    def __str__(self):
        return str(self.id)


