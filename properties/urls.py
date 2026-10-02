from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/add/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_update, name='property_update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('property/<int:pk>/request/', views.send_request, name='send_request'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('requests/', views.rental_request_list, name='rental_request_list'),
    path('request/<int:pk>/status/', views.update_request_status, name='update_request_status'),
]