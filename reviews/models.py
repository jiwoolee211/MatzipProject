from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator 
from restaurants.models import Restaurant 
from django.contrib.auth.models import User

class Review(models.Model):
    # 어떤 식당에 대한 리뷰인지 연결
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    #이미지 추가
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)

    #작성자 연결
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    # 리뷰 내용
    content = models.TextField()
    # 2. 별점에 최소 1, 최대 5 제한 걸기!!!!
    rating = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # 작성일
    created_at = models.DateTimeField(auto_now_add=True)
    #수정일
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.content[:10]}"