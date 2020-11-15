from django.contrib import admin
from django.http import HttpResponseRedirect

from cart.models import Cart, Item
from cart.tasks import print_document


class ItemTabular(admin.TabularInline):
    model = Item
    extra = 1


class CartAdmin(admin.ModelAdmin):
    inlines = [ItemTabular, ]
    change_form_template = 'cart/change_form.html'

    def response_change(self, request, obj):
        if "print-document" in request.POST:
            print_document.delay(obj.pk)
            self.message_user(request, "Документ отправлен на печать")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


admin.site.register(Cart, CartAdmin)
