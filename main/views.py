from django.shortcuts import render
from django.db.models import Count, Avg

from restaurants.models import Restaurant


def home(request):
    popular_restaurants = Restaurant.objects.prefetch_related('images').annotate(
        bucket_count=Count('bucketlist'),
        avg_rating=Avg('comments__rating'),
        comment_count=Count('comments')
    ).order_by('-bucket_count', '-avg_rating', '-comment_count')[:3]

    return render(request, 'main/index.html', {
        'popular_restaurants': popular_restaurants,
    })