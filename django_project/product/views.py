from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView
from pure_pagination import PaginationMixin

from account.models import User
from cart.cart import Cart
from cart.models import Cart as CartModel
from product.models import Product


class ProductListView(PaginationMixin, ListView):
    template_name = "product/product_list.html"
    model = Product
    context_object_name = 'products'
    paginate_by = 15

    def get_template_names(self):
        if not self.request.user.is_anonymous and self.request.user.role == self.request.user.MANAGER:
            return "cart/client_cart_list.html"
        return "product/product_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous and self.request.user.role == self.request.user.CLIENT:
            cart = Cart(self.request)
            context['count'] = cart.count()
        else:
            context['clients'] = User.objects.filter(role=User.CLIENT).prefetch_related('cart_set')
            context['total'] = context['clients'].first().cart_set.first().total()
            context['items'] = context['clients'].first().cart_set.first().item_set.all()
        return context


class ProductDetailView(DetailView):
    template_name = "product/product_detail.html"
    model = Product
    context_object_name = 'product'
    slug_field = 'sku'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['count'] = cart.count()
        return context


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.update(product, quantity, product.retail_price)
        return JsonResponse({'ok': True, 'count': cart.count()})
    return JsonResponse({'ok': False})


def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.remove(product)
        return JsonResponse({'ok': True, 'count': cart.count(), 'total': cart.summary()})
    return JsonResponse({'ok': False})
