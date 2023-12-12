
from django.urls import path
from . import views

urlpatterns = [
    path('tenders/add/', views.add_tender, name = 'add_tender'),
    path('tender/<int:id>/', views.tender_profile, name = 'tender_profile'),
    path('tender/<int:id>/update/', views.tender_update, name = 'tender_update'),
    path('tender/<int:id>/delete/', views.tender_delete, name = 'tender_delete'),
    path('tenders/list/', views.tenders_list, name = 'tenders_list'),
    
    path('tenders/add-question/', views.add_question, name = 'add_question'),
    path('tenders/question/<int:id>/delete/', views.delete_question, name = 'delete_question'),
    path('tenders/question/<int:id>/update/', views.update_question, name = 'update_question'),
    
    
    path('tenders/question/add-choice/', views.add_choice, name = 'add_choice'),
    path('tenders/choice/<int:id>/delete/', views.delete_choice, name = 'delete_choice'),
    

]