from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_list, name='restaurant_list'),       # 127.0.0.1:8000/restaurants/
    path('create/', views.restaurant_create, name='restaurant_create'), # 127.0.0.1:8000/restaurants/create/
]