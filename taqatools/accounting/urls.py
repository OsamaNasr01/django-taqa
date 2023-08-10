
from django.urls import path
from . import views

urlpatterns = [
    path('accounting/', views.accounting, name='accounting'),
    path('accounting/sale_invoice/add', views.add_s_invoice, name='add_s_invoice')
]