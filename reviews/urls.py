from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.review_create, name='review_create'), # 127.0.0.1:8000/reviews/create/
    path('list/', views.review_list, name='review_list'),
    path('detail/<int:review_id>/', views.review_detail, name='review_detail'),
    path('update/<int:review_id>/', views.review_update, name='review_update'),
    path('delete/<int:review_id>/', views.review_delete, name='review_delete'),
]