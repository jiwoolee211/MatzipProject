from django.db import models

# Create your models here.

from restaurants.models import Restaurant 

class Review(models.Model):
    # 어떤 식당에 대한 리뷰인지 연결
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    # 리뷰 내용
    content = models.TextField()
    # 별점 (1~5점)
    rating = models.IntegerField(default=5)
    # 작성일
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.content[:10]}"