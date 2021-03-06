from django import forms

from cart.models import Item


class ProductUpdateForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['cart', 'product', 'quantity', 'unit_price']
