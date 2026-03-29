from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm  
from .forms import RestaurantForm

# 1. [CREATE] 리뷰 작성 
# reviews/views.py
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})

# 2. [READ] 리뷰 목록 조회 
def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

# 3. [READ] 리뷰 상세 조회 
def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})

# 4. [UPDATE] 리뷰 수정 
def review_update(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES,instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form})

# 5. [DELETE] 리뷰 삭제 (추가)
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('review_list')

# 이미지 추가하도록
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = RestaurantForm() 
        
    return render(request, 'reviews/restaurant_create.html', {'form': form})