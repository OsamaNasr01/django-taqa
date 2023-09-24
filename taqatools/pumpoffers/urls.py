
from django.urls import path
from . import views

urlpatterns = [
    path('pump-offer/request/', views.pump_offer_request, name='pump_offer_request'),
    path('pump-offer/gov-select/', views.gov_select, name='gov_select'),
    
]