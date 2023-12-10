
from django.urls import path
from . import views

urlpatterns = [
    path('tenders/add/', views.add_tender, name = 'add_tender'),
    path('tender/<int:id>/', views.tender_profile, name = 'tender_profile'),

]