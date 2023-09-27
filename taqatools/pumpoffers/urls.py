
from django.urls import path
from . import views

urlpatterns = [
    path('pump-offer/request/', views.pump_offer_request, name='pump_offer_request'),
    path('pump-offer/gov-select/', views.gov_select, name='gov_select'),
    path('pump-offer/requests/list/', views.pumpoffer_request_list, name='pumpoffer_request_list'),
    path('pump-offer/requests/<int:id>/', views.pumpoffer_request_profile, name='pumpoffer_request_profile'),
    
    path('pump-offer/pump-selection/', views.pump_selection, name='pump_selection'),
    path('pump-offer/add-pump-to-offer/', views.add_pump_to_offer, name='add_pump_to_offer'),
    path('pump-offer/remove-pump-from-offer/', views.remove_pump_from_offer, name='remove_pump_from_offer'),
    
    path('pump-offer/motor-selection/', views.motor_selection, name='motor_selection'),
    path('pump-offer/add-motor-to-offer/', views.add_motor_to_offer, name='add_motor_to_offer'),
    path('pump-offer/remove-motor-from-offer/', views.remove_motor_from_offer, name='remove_motor_from_offer'),
    
    path('pump-offer/pipes-selection/', views.pipes_selection, name='pipes_selection'),
    path('pump-offer/adaptors-selection/', views.adaptors_selection, name='adaptors_selection'),
    path('pump-offer/cable-selection/', views.cable_selection, name='cable_selection'),
    path('pump-offer/control-panel-selection/', views.control_panel_selection, name='control_panel_selection'),
    path('pump-offer/instalation-evaluation/', views.install_evaluatation, name='install_evaluatation'),
    
]