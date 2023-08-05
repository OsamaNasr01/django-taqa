
from django.urls import path
from . import views

urlpatterns = [
    # Category routes 
    path('product/categories/', views.p_category_list, name='p_category_list'),
    path('product/categories/add/', views.add_p_category, name='add_p_category'),
    path('product/category/<slug:slug>/', views.p_category_profile, name='p_category_profile'),
    path('product/category/update/<slug:slug>/', views.update_p_category, name='update_p_category'),
    path('product/category/delete/<slug:slug>/', views.delete_p_category, name='delete_p_category'),
    # Product routes
    path('product/add/', views.add_product, name='add_product'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('product/update/<slug:slug>/', views.update_product, name='update_product'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),
    # Brands routes
    path('product/brand/all/', views.brands, name='brands'),
    path('product/brand/add/', views.add_brand, name='add_brand'),
    path('product/brand/<slug:slug>/', views.brand_profile, name='brand_profile'),
    path('product/brand/update/<slug:slug>/', views.update_brand, name='update_brand'),
    path('product/brand/delete/<slug:slug>/', views.delete_brand, name='delete_brand'),
    # price routes
    path('product/price/update/<slug:slug>/', views.update_price, name='update_price'),
    # Specs routes
    path('product/specs/add/', views.add_spec, name='add_spec'),
    path('product/specs/update/<int:id>', views.update_spec, name='update_spec'),
    path('product/specs/delete/<int:id>', views.delete_spec, name='delete_spec'),

]