from django import forms
from .models import Restaurant, Comment


# 여러 파일 업로드를 지원하는 커스텀 위젯
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


# 여러 파일을 받는 커스텀 필드
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={
            'class': 'form-control'
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean

        if isinstance(data, (list, tuple)):
            result = [single_file_clean(file, initial) for file in data]
        else:
            result = single_file_clean(data, initial)

        return result


class RestaurantForm(forms.ModelForm):
    extra_images = MultipleFileField(
        required=False,
        label='추가 이미지'
    )

    class Meta:
        model = Restaurant
        fields = ['name', 'category', 'location', 'address', 'description', 'image']

        labels = {
            'name': '맛집 이름',
            'category': '카테고리',
            'location': '지역',
            'address': '주소',
            'description': '설명',
            'image': '대표 이미지',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '맛집 이름을 입력하세요'
            }),

            'category': forms.Select(attrs={
                'class': 'form-select'
            }),

            'location': forms.Select(attrs={
                'class': 'form-select'
            }),

            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '예: 서울시 성북구 푸킷동 123-45'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '맛집에 대한 설명을 입력하세요!'
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'rating']

        labels = {
            'comment': '댓글 내용',
            'rating': '별점',
        }

        widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '댓글을 남겨주세요.'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 별점 선택 안 해도 되게 만들기
        self.fields['rating'].required = False
        self.fields['rating'].empty_label = '별점 선택 안 함'