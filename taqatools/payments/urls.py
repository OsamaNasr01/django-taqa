
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name = 'checkout'),
    path('wallet/<str:gate>/', views.payment_proccess, name = 'payment_proccess'),
]