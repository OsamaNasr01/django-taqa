
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
    
    path('pump-offer/pipe-selection/', views.pipe_selection, name='pipe_selection'),
    path('pump-offer/add-pipe-to-offer/', views.add_pipe_to_offer, name='add_pipe_to_offer'),
    path('pump-offer/remove-pipe-from-offer/', views.remove_pipe_from_offer, name='remove_pipe_from_offer'),
    
    
    path('pump-offer/adaptors-selection/', views.adaptor_selection, name='adaptor_selection'),
    path('pump-offer/add-adaptor-to-offer/', views.add_adaptor_to_offer, name='add_adaptor_to_offer'),
    path('pump-offer/remove-adaptor-from-offer/', views.remove_adaptor_from_offer, name='remove_adaptor_from_offer'),
    
    path('pump-offer/cable-selection/', views.cable_selection, name='cable_selection'),
    path('pump-offer/add-cable-to-offer/', views.add_cable_to_offer, name='add_cable_to_offer'),
    path('pump-offer/remove-cable-from-offer/', views.remove_cable_from_offer, name='remove_cable_from_offer'),
    
    path('pump-offer/control-panel-selection/', views.control_panel_selection, name='control_panel_selection'),
    path('pump-offer/instalation-evaluation/', views.install_evaluatation, name='install_evaluatation'),
    
]