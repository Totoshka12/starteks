from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from cart.cart import Cart


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    cart = Cart(request)
    cart.cart.user = user
    cart.cart.save()
