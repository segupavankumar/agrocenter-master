from django.urls import path
from . import views

urlpatterns = [
path('', views.shop,name = 'shop'),
path('cart',views.cart_,name='cart'),
path('create_cart',views.create_cart,name='create'),
path('remove_from_user_cart',views.remove_from_user_cart,name='remove'),
path('update_cart',views.update_cart,name="updatecart"),
path('checkout',views.checkout,name='checkout'),
path('order_create',views.order_creation,name='order'),
path('payment_status',views.payment_status,name='status')
]
