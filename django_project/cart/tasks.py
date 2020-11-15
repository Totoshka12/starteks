from __future__ import unicode_literals

import os

from wkhtmltopdf import render_pdf_from_template

from cart.models import Cart
from starteks.celery import app
from django.conf import settings


@app.task
def print_document(pk):
    cart = Cart.objects.select_related('user').filter(pk=pk).first()
    if cart:
        items = cart.item_set.all()
        context = {
            'items': items,
            'fio': cart.user.full_name(),
            'order': cart.id,
            'address': cart.user.address,
            'total': cart.total(),
        }
        html = render_pdf_from_template(
            input_template='cart_to_pdf.html',
            header_template=None,
            footer_template=None,
            context=context)
        filename = os.path.join(settings.MEDIA_ROOT, 'order_{}.pdf'.format(cart.id))
        file = open(filename, 'wb')
        file.write(html)
        file.close()
        return os.path.getmtime(filename)
