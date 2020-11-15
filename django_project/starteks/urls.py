"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from cart.views import CartList, OrderList, OrderDetail, make_order
from product.views import ProductListView, ProductDetailView, add_to_cart, remove_from_cart

urlpatterns = [
    path('', ProductListView.as_view(), name="home"),
    path('cart/', CartList.as_view(), name="cart-list"),
    path('orders/', OrderList.as_view(), name="order-list"),
    path('orders/make/<int:pk>', make_order, name="make-order"),
    path('orders/<int:pk>', OrderDetail.as_view(), name="order-detail"),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', remove_from_cart, name='remove_from_cart'),
    path('account/', include('registration.backends.default.urls')),
    path('admin/', admin.site.urls),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
