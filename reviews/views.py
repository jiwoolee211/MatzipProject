from django.shortcuts import render, redirect, get_object_or_404
from .models import Review, ReviewImage
from .forms import ReviewForm, RestaurantForm

def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/review_list.html', {'reviews': reviews})


def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        files = request.FILES.getlist('images') 
        
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.author = request.user
            review.save()

            for f in files:
                ReviewImage.objects.create(review=review, image=f)
                
            
            return redirect('reviews:review_list') 
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def review_update(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        files = request.FILES.getlist('images')
        
        if form.is_valid():
            review = form.save()
            if files: 
                for f in files:
                    ReviewImage.objects.create(review=review, image=f)
            return redirect('reviews:review_detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form})


def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    review.delete()
    return redirect('reviews:review_list')