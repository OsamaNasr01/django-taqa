
from django.urls import path
from . import views

urlpatterns = [
    path('tenders/add/', views.add_tender, name = 'add_tender'),
    path('tender/<int:id>/', views.tender_dashboard, name = 'tender_dashboard'),
    path('tender/<int:id>/update/', views.tender_update, name = 'tender_update'),
    path('tender/<int:id>/delete/', views.tender_delete, name = 'tender_delete'),
    path('tender/<int:id>/profile/', views.tender_profile, name = 'tender_profile'),
    path('tenders/list/', views.tenders_list, name = 'tenders_list'),
    
    path('tenders/add-question/', views.add_question, name = 'add_question'),
    path('tenders/question/<int:id>/delete/', views.delete_question, name = 'delete_question'),
    path('tenders/question/<int:id>/update/', views.update_question, name = 'update_question'),
    
    
    path('tenders/question/add-choice/', views.add_choice, name = 'add_choice'),
    path('tenders/choice/<int:id>/delete/', views.delete_choice, name = 'delete_choice'),
    path('tenders/choice/<int:id>/update/', views.update_choice, name = 'update_choice'),
    
    
    path('tenders/add-category/', views.add_category_to_tender, name = 'add_category_to_tender'),
    path('tenders/category/<int:id>/delete/', views.delete_category_from_tender, name = 'delete_category_from_tender'),
    
    
    path('tender/<int:id>/request/', views.tender_request, name = 'tender_request'),
    path('tender-request/<int:id>', views.tender_request_profile, name = 'tender_request_profile'),
    
    path('tender-request/add-offer/', views.add_offer, name = 'add_offer'),
    path('tender-offer/<int:id>/product-selection/', views.product_selection, name = 'product_selection'),
    path('tender-offer/add-product/', views.add_product_offer, name = 'add_product_offer'),
    path('tender-offer/remove-product/', views.remove_product_offer, name = 'remove_product_offer'),
    path('tender-offer/confirm-offer/', views.confirm_offer, name = 'confirm_offer'),
    
]