
from django.urls import path
from . import views

urlpatterns = [
    # Category routes 
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('return/', views.return_policy, name='return'),
]