from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    # 카테고리 선택지
    CATEGORY_CHOICES = [
        ('KOR', '한식'),
        ('CHI', '중식'),
        ('JPN', '일식'),
        ('WES', '양식'),
        ('DES', '디저트'),
        ('MEAT', '고기/구이'),
        ('BAR', '술집'),
        ('ETC', '기타'),
    ]

    # 시/도 단위 지역 선택지
    LOCATION_CHOICES = [
        ('SEOUL', '서울'),
        ('GYEONGGI', '경기'),
        ('INCHEON', '인천'),
        ('BUSAN', '부산'),
        ('DAEGU', '대구'),
        ('DAEJEON', '대전'),
        ('GWANGJU', '광주'),
        ('ULSAN', '울산'),
        ('SEJONG', '세종'),
        ('GANGWON', '강원'),
        ('CHUNGBUK', '충북'),
        ('CHUNGNAM', '충남'),
        ('JEONBUK', '전북'),
        ('JEONNAM', '전남'),
        ('GYEONGBUK', '경북'),
        ('GYEONGNAM', '경남'),
        ('JEJU', '제주'),
        ('ETC', '기타'),
    ]

    name = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='KOR')
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='SEOUL')
    address = models.CharField(max_length=100, help_text="상세 주소를 입력하세요")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='restaurants/', null=True, blank=True)

    # 작성자
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='restaurants',
        null=True,
        blank=True
    )

    # 등록일
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    RATING_CHOICES = [
        (1, '⭐ 1점'),
        (2, '⭐⭐ 2점'),
        (3, '⭐⭐⭐ 3점'),
        (4, '⭐⭐⭐⭐ 4점'),
        (5, '⭐⭐⭐⭐⭐ 5점'),
    ]

    comment = models.CharField(max_length=200)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True
    )
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.comment


class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='restaurants/detail/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} 이미지"