from django.urls import path
from .views import CartView, CartItemAddView, CartItemDetailView, CartClearView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart_detail'),
    path('cart/add/', CartItemAddView.as_view(), name='cart_add'),
    path('cart/items/<int:product_id>/', CartItemDetailView.as_view(), name='cart_item_detail'),
    path('cart/clear/', CartClearView.as_view(), name='cart_clear'),
]
