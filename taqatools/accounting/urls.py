
from django.urls import path
from . import views

urlpatterns = [
    path('accounting/', views.accounting, name='accounting'),
    path('accounting/sale_invoice/add', views.add_s_invoice, name='add_s_invoice'),
    path('accounting/add-product-to-cart/', views.add_product_cart, name='add_product_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete_cart_item/', views.delete_cart_item, name= 'delete_cart_item'),
    path('cart/update_cart_item/', views.update_cart_item, name='update_cart_item'),
    
]