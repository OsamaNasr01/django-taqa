
from django.urls import path
from . import views

urlpatterns = [
    path('accounting/', views.accounting, name='accounting'),
    path('accounting/sale_invoice/add', views.add_s_invoice, name='add_s_invoice'),
    
    path('accounting/add-product-to-cart/', views.add_product_cart, name='add_product_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/delete_cart_item/', views.delete_cart_item, name= 'delete_cart_item'),
    path('cart/update_cart_item/', views.update_cart_item, name='update_cart_item'),
    
    path('cart/search-users/', views.search_users, name='search_users'),
    
    path('cart/add-offer/', views.add_offer, name = 'add_offer'),
    path('accounting/offer/<int:id>', views.offer_profile, name='offer_profile'),
    path('accounting/offer/<int:id>/update', views.offer_update, name='offer_update'),
    path('accounting/offer/<int:id>/delete', views.offer_delete, name='offer_delete'),
    path('accounting/offers/', views.offers, name='offers'),
    path('members/<slug:username>/offers', views.user_offers, name = 'user_offers'),
    
    
    path('cart/add-sale/', views.add_sale, name='add_sale'),
    path('accounting/sale/<int:id>/', views.sale_profile, name='sale_profile'),
    path('accounting/sale/<int:id>/update', views.sale_update, name='sale_update'),
    path('accounting/sale/<int:id>/delete', views.sale_delete, name='sale_delete'),
    path('accounting/sales/', views.sales, name='sales'),
    path('members/<slug:username>/sales', views.user_sales, name = 'user_sales'),
    
    path('cart/add-purchase/', views.add_purchase, name='add_purchase'),
    path('accounting/purchase/<int:id>/', views.purchase_profile, name='purchase_profile'),
    path('accounting/purchase/<int:id>/update', views.purchase_update, name='purchase_update'),
    path('accounting/purchase/<int:id>/delete', views.purchase_delete, name='purchase_delete'),
    path('accounting/purchases/', views.purchases, name='purchases'),
    path('members/<slug:username>/purchases', views.user_purchases, name = 'user_purchases'),
    
    path('accounting/<slug:username>/add-payment/', views.add_payment, name = 'add_payment'),
    path('accounting/payment/<int:id>/', views.payment_profile, name='payment_profile'),
    path('accounting/payment/<int:id>/update', views.payment_update, name='payment_update'),
    path('accounting/payment/<int:id>/delete', views.payment_delete, name='payment_delete'),
    path('accounting/payments/', views.payments, name='payments'),
    path('members/<slug:username>/payments', views.user_payments, name = 'user_payments'),
    
    path('accounting/<slug:username>/add-receipt/', views.add_receipt, name = 'add_receipt'),
    path('accounting/receipt/<int:id>/', views.receipt_profile, name='receipt_profile'),
    path('accounting/receipt/<int:id>/update', views.receipt_update, name='receipt_update'),
    path('accounting/receipt/<int:id>/delete', views.receipt_delete, name='receipt_delete'),
    path('accounting/receipts/', views.receipts, name='receipts'),
    path('members/<slug:username>/receipts', views.user_receipts, name = 'user_receipts'),
    
]