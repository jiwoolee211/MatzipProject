# buckets/urls.py
from django.urls import path
from . import views

app_name = 'buckets'

urlpatterns = [
    path('', views.bucket_list, name='list'),
    path('add/<int:restaurant_id>/', views.add_bucket, name='add'),
    path('delete/<int:bucket_id>/', views.delete_bucket, name='delete'),
    path('memo/<int:restaurant_id>/', views.update_bucket_memo, name='update_memo'),
]