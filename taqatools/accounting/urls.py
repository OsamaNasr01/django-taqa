
from django.urls import path
from . import views

urlpatterns = [
    path('accounting/', views.accounting, name='accounting'),
    path('accounting/sale_invoice/add', views.add_s_invoice, name='add_s_invoice'),
    path('accounting/add-product-to-cart/', views.add_product_cart, name='add_product_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete_cart_item/', views.delete_cart_item, name= 'delete_cart_item'),
    path('cart/update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('cart/add-offer/', views.add_offer, name='add_offer'),
    path('cart/search-users/', views.search_users, name='search_users'),
    path('accounting/offers/', views.offers, name='offers'),
    path('accounting/offer/<int:id>', views.offer_profile, name='offer_profile'),
    path('members/<slug:username>/offers', views.user_offers, name = 'user_offers'),
    
]