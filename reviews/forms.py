from django import forms
from .models import Review, Restaurant 

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ReviewForm(forms.ModelForm):
    
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}), 
        required=False,
        label="맛집 사진 (여러 장 선택 가능)"
    )

    class Meta:
        model = Review
        fields = ['restaurant', 'content', 'rating', 'mood_tag'] 
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': '맛은 어땠나요?', 'class': 'form-control', 'rows': 5}),
            'mood_tag': forms.TextInput(attrs={'placeholder': '#가성비', 'class': 'form-control'}),
        }

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'location', 'address', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '상세 주소를 입력하세요'}),
        }