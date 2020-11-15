from django.db import models
from djmoney.models.fields import MoneyField
from easy_thumbnails.fields import ThumbnailerImageField


class Product(models.Model):
    sku = models.CharField(verbose_name='Артикул', max_length=255)
    title = models.CharField(verbose_name='Наименование', max_length=255)
    purchase_price = MoneyField(verbose_name='Закупочная цена', max_digits=14, decimal_places=2, default_currency='RUB')
    retail_price = MoneyField(verbose_name='Розничная цена', max_digits=14, decimal_places=2, default_currency='RUB')
    supplier_price = MoneyField(verbose_name='Цена поставщика', max_digits=14, decimal_places=2, default_currency='RUB')
    photo = ThumbnailerImageField(upload_to='photos', blank=True)

    def __str__(self):
        return '{}: {}'.format(self.title, self.retail_price)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
