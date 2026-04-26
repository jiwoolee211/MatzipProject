from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from django.contrib.auth.models import User
from restaurants.models import Restaurant 

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    content = models.TextField()
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # 태그 추가 (예: #가성비 #분위기맛집)
    mood_tag = models.CharField(max_length=50, blank=True, help_text="분위기 태그 (예: 데이트, 가성비)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}의 {self.restaurant.name} 리뷰"

# 다중 이미지를 위한 별도 모델
class ReviewImage(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='reviews/')

    def __str__(self):
        return f"{self.review.restaurant.name} - 이미지"