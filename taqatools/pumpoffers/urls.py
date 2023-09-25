
from django.urls import path
from . import views

urlpatterns = [
    path('pump-offer/request/', views.pump_offer_request, name='pump_offer_request'),
    path('pump-offer/gov-select/', views.gov_select, name='gov_select'),
    path('pump-offer/requests/list/', views.pumpoffer_request_list, name='pumpoffer_request_list'),
    path('pump-offer/requests/<int:id>/', views.pumpoffer_request_profile, name='pumpoffer_request_profile'),
    
]