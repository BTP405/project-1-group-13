from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('person/<str:pk>/', views.person, name="person"),
    path('update/<str:pk>/', views.update, name="update"),
    path('add/', views.add, name="add"),
    path('delete/<str:pk>/', views.delete_contact, name="delete_contact")  # Update this line
]
