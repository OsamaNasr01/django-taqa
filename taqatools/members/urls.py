
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # deal with members register/read/update/delete - login/logout
    path('register/', views.register_user, name = 'register'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('members/<slug:username>/', views.user_profile, name = 'user_profile'),
    path('members/', views.users, name = 'users'),
    # deal with companies add/read/update/delete
    path('company/add/', views.add_company, name = 'add_company'),
    path('company/update/<slug:slug>/', views.update_company, name = 'update_company'),
    path('company/delete/<slug:slug>/', views.delete_company, name = 'delete_company'),
    path('company/<slug:slug>/', views.co_profile, name = 'co_profile'),
    path('companies/', views.co_list, name = 'companies'),
    # deal with company categories add/read/update/delete
    path('company/category/add/', views.add_co_category, name = 'add_co_category'),
    path('company/category/update/<slug:slug>', views.update_co_category, name = 'update_co_category'),
    path('company/category/delete/<slug:slug>', views.delete_co_category, name = 'delete_co_category'),
    path('company/category/all/', views.co_category_list, name = 'co_category_list'),
    path('company/category/<slug:slug>/', views.co_category_profile, name='co_category_profile')
]