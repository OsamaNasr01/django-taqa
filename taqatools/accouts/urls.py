from django.urls import path
from . import views

urlpatterns = [
    path('invoice/add/', views.invoice_add, name='invoice_add'),
    path('invoice/add_h1/', views.add_h1, name='add_h1'),
    
]