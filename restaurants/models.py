from django.db import models

# Create your models here.


class Restaurant(models.Model):
    # 식당 이름
    name = models.CharField(max_length=50)
    # 음식 종류 (한식, 일식 등)
    category = models.CharField(max_length=20)
    # 식당 위치
    location = models.CharField(max_length=100)
    # 식당 한줄 설명 
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name