from django import forms
from .models import Review, Restaurant

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant', 'content', 'rating','image'] 
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 5}), #별점 5점 위로 안올라가게
        }

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        # 지우님의 Restaurant 모델 필드명에 맞춰서 적어주세요 (name, location 등)
        fields = ['name', 'category', 'location', 'description', 'image']