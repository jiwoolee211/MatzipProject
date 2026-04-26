from django.db import models
from django.conf import settings
from restaurants.models import Restaurant

class BucketList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_visited = models.BooleanField(default=False) # 방문 완료 체크
    priority = models.IntegerField(default=3) # 1~5 우선순위
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 한 유저가 같은 식당을 여러 번 담지 못하게 설정! 
        unique_together = ('user', 'restaurant')

    def __str__(self):
        return f"{self.user.username}의 버킷: {self.restaurant.name}"