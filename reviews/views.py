from django.shortcuts import render, redirect
from .forms import ReviewForm

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_create.html', {'form': form})