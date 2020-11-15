from django.db import models
from django.db.models import Sum, F
from django.conf import settings
from djmoney.models.fields import MoneyField

from account.models import User
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name='Дата создания')
    checked_out = models.BooleanField(default=False, verbose_name='Отправленно')

    def total(self):
        return self.item_set.all().aggregate(total=Sum(F('quantity') * F('unit_price'), output_field=MoneyField())).get('total', 0)

    def title(self):
        return 'Заказ №{}: от {}'.format(self.pk, self.creation_date)

    def pdf_url(self):
        return '{}order_{}.pdf'.format(settings.MEDIA_URL, self.pk)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзинаы'
        ordering = ('-creation_date',)

    def __str__(self):
        return '{}'.format(self.creation_date)


class Item(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количнство')
    unit_price = MoneyField(verbose_name='Цена за штуку', max_digits=14, decimal_places=2, default_currency='RUB')

    class Meta:
        verbose_name = 'Продукт в корзине'
        verbose_name_plural = 'Продукты в корзине'
        ordering = ('cart', )

    def total_price(self):
        return self.quantity * self.unit_price
    total_price = property(total_price)
