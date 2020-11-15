import csv
import decimal

from django import forms
from django.contrib import admin
import urllib.request
import codecs

from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import path, reverse
from djmoney.money import Money

from product.models import Product


class ProductImportForm(forms.Form):
    product_file = forms.FileField(label='CSV файл', required=False)
    product_url = forms.URLField(label='URL на CSV файл', required=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = 'product/change_list.html'
    readonly_fields = ['retail_price', 'purchase_price']
    list_display = ['sku', 'title', 'retail_price']

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import_product/', self.import_product),
        ]
        return my_urls + urls

    @transaction.atomic
    def import_product(self, request):
        if request.method == "POST":
            form = ProductImportForm(request.POST, request.FILES)
            if form.is_valid():
                product_file = form.cleaned_data['product_file']
                product_url = form.cleaned_data['product_url']
                if product_file:
                    file = product_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(file, delimiter=';')
                elif product_url:
                    stream = urllib.request.urlopen(product_url)
                    reader = csv.DictReader(codecs.iterdecode(stream, 'utf-8'), delimiter=';')
                else:
                    self.message_user(request, "Не выбрано от куда импортировать")
                    return redirect("..")
                for row in reader:
                    sp = Money(row['Цена'], 'RUB')
                    rp = Money(decimal.Decimal(1.2)*sp.amount, 'RUB') if sp.amount < 1000 else Money(decimal.Decimal(1.1)*sp.amount, 'RUB')
                    Product.objects.create(
                        sku=row['Код товара'],
                        title=row['Наименование'],
                        supplier_price=sp,
                        purchase_price=Money(decimal.Decimal(0.9)*sp.amount, 'RUB'),
                        retail_price=rp,
                    )
                self.message_user(request, "Продукты имортированы")
                return redirect("..")
        form = ProductImportForm()
        payload = {"form": form}
        return render(
            request, "product/import_product.html", payload
        )

    def save_model(self, request, obj, form, change):
        sp = obj.supplier_price.amount
        obj.purchase_price = decimal.Decimal(0.9)*sp
        obj.retail_price = decimal.Decimal(1.2)*sp if sp < 1000 else decimal.Decimal(1.1)*sp
        super().save_model(request, obj, form, change)
