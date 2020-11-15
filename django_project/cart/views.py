from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView

from account.models import User
from cart.cart import Cart
from cart.models import Item, Cart as CartModel
from cart.tasks import print_document


class CartList(ListView):
    template_name = 'cart/cart_list.html'
    queryset = Item.objects.all()
    context_object_name = "items"
    cart = None

    def get_queryset(self):
        self.cart = Cart(self.request)
        return self.queryset.select_related('product').filter(cart=self.cart.cart)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart.cart
        context['total'] = self.cart.summary()
        context['count'] = self.cart.count()
        return context


class OrderList(ListView):
    context_object_name = 'orders'
    template_name = 'cart/order_list.html'

    def get_queryset(self):
        return CartModel.objects.filter(user=self.request.user, checked_out=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        order = context['orders'].first()
        cart = Cart(self.request)
        context['total'] = cart.summary()
        context['count'] = cart.count()
        context['pk'] = cart.cart.pk
        if order:
            context['items'] = order.item_set.all()
        return context


class OrderDetail(DetailView):
    template_name = 'cart/order_list.html'
    context_object_name = 'order'
    model = CartModel

    def get_template_names(self):
        if self.request.user.role == self.request.user.MANAGER:
            return "cart/client_cart_list.html"
        return self.template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == self.request.user.CLIENT:
            cart = Cart(self.request)
            context['orders'] = CartModel.objects.filter(user=self.request.user, checked_out=True)
            context['count'] = cart.count()
        else:
            context['clients'] = User.objects.filter(role=User.CLIENT).prefetch_related('cart_set')
        context['items'] = context['order'].item_set.all()
        context['total'] = context['order'].total()
        context['pk'] = context['order'].pk
        return context


def make_order(request, pk):
    cart = CartModel.objects.filter(pk=pk).first()
    if cart:
        cart.checked_out = True
        cart.save()
        print_document.delay(cart.pk)
    return redirect(reverse('order-detail', kwargs={'pk': pk}))
