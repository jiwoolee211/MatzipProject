from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q, Avg

from .models import Restaurant, Comment, RestaurantImage
from buckets.models import BucketList
from .forms import RestaurantForm, CommentForm


# 1. 맛집 목록 페이지
def restaurant_list(request):
    restaurants = Restaurant.objects.prefetch_related('images').all()

    # 검색어
    query = request.GET.get('q', '')

    # 카테고리 필터
    category = request.GET.get('category', '')

    # 지역 필터
    location = request.GET.get('location', '')

    # 정렬
    sort = request.GET.get('sort', 'latest')

    # 검색 기능: 이름, 주소, 설명에서 검색
    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(description__icontains=query)
        )

    # 카테고리 필터
    if category:
        restaurants = restaurants.filter(category=category)

    # 지역 필터
    if location:
        restaurants = restaurants.filter(location=location)

    # 정렬 기능
    if sort == 'oldest':
        restaurants = restaurants.order_by('created_at')
    elif sort == 'name':
        restaurants = restaurants.order_by('name')
    else:
        restaurants = restaurants.order_by('-created_at')

    paginator = Paginator(restaurants, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'restaurants/restaurant_list.html', {
        'restaurants': posts,
        'query': query,
        'selected_category': category,
        'selected_location': location,
        'selected_sort': sort,
        'category_choices': Restaurant.CATEGORY_CHOICES,
        'location_choices': Restaurant.LOCATION_CHOICES,
    })


# 2. 맛집 제보(생성)
@login_required(login_url='accounts:login')
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)

        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.author = request.user
            restaurant.save()

            # 추가 이미지 여러 장 저장
            for img in request.FILES.getlist('extra_images'):
                RestaurantImage.objects.create(
                    restaurant=restaurant,
                    image=img
                )

            return redirect('restaurant_list')

    else:
        form = RestaurantForm()

    return render(request, 'restaurants/restaurant_create.html', {
        'form': form
    })


# 3. 맛집 상세 페이지
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant.objects.prefetch_related('images'),
        pk=pk
    )

    comments = restaurant.comments.all().order_by('-date')
    comment_form = CommentForm()

    bucket_count = BucketList.objects.filter(restaurant=restaurant).count()

    # 별점이 있는 댓글만 평균 계산
    avg_rating = restaurant.comments.filter(
        rating__isnull=False
    ).aggregate(avg=Avg('rating'))['avg']

    is_bucketed = False
    user_bucket = None

    if request.user.is_authenticated:
        user_bucket = BucketList.objects.filter(
            user=request.user,
            restaurant=restaurant
        ).first()

        is_bucketed = user_bucket is not None

    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'comments': comments,
        'comment_form': comment_form,
        'bucket_count': bucket_count,
        'avg_rating': avg_rating,
        'is_bucketed': is_bucketed,
        'user_bucket': user_bucket,
    })


# 4. 댓글 작성
@login_required(login_url='accounts:login')
def create_comment(request, res_id):
    restaurant = get_object_or_404(Restaurant, pk=res_id)

    if request.method == "POST":
        filled_form = CommentForm(request.POST)

        if filled_form.is_valid():
            finished_form = filled_form.save(commit=False)
            finished_form.article = restaurant
            finished_form.author = request.user
            finished_form.save()

    return redirect('restaurant_detail', pk=res_id)


# 5. 댓글 삭제
@login_required(login_url='accounts:login')
def comment_delete(request, restaurant_id, comment_id):
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        article_id=restaurant_id
    )

    # 댓글 작성자만 삭제 가능
    if comment.author != request.user:
        return redirect('restaurant_detail', pk=restaurant_id)

    if request.method == 'POST':
        comment.delete()

    return redirect('restaurant_detail', pk=restaurant_id)


# 6. 댓글 수정
@login_required(login_url='accounts:login')
def comment_update(request, restaurant_id, comment_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    comment = get_object_or_404(Comment, pk=comment_id, article=restaurant)

    # 댓글 작성자만 수정 가능
    if comment.author != request.user:
        return redirect('restaurant_detail', pk=restaurant_id)

    if request.method == "POST":
        new_text = request.POST.get('comment_text')
        new_rating = request.POST.get('rating')

        if new_text:
            comment.comment = new_text

        if new_rating:
            comment.rating = new_rating
        else:
            comment.rating = None

        comment.save()

        return redirect('restaurant_detail', pk=restaurant_id)

    return render(request, 'restaurants/update_comment.html', {
        'comment': comment,
        'restaurant': restaurant,
    })


# 7. 맛집 삭제
@login_required(login_url='accounts:login')
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if request.method == 'POST':
        restaurant.delete()
        return redirect('restaurant_list')

    return redirect('restaurant_detail', pk=pk)


# 8. 맛집 수정
@login_required(login_url='accounts:login')
def restaurant_update(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)

        if form.is_valid():
            updated_restaurant = form.save(commit=False)

            if not updated_restaurant.author:
                updated_restaurant.author = request.user

            updated_restaurant.save()

            # 수정 페이지에서도 추가 이미지 더 업로드 가능
            for img in request.FILES.getlist('extra_images'):
                RestaurantImage.objects.create(
                    restaurant=updated_restaurant,
                    image=img
                )

            return redirect('restaurant_detail', pk=pk)

    else:
        form = RestaurantForm(instance=restaurant)

    return render(request, 'restaurants/restaurant_create.html', {
        'form': form,
        'edit_mode': True,
        'restaurant': restaurant,
    })


# 9. 버킷 추가 / 취소
@login_required(login_url='accounts:login')
def toggle_bucket(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)

    bucket_item = BucketList.objects.filter(
        user=request.user,
        restaurant=restaurant
    )

    if bucket_item.exists():
        bucket_item.delete()
    else:
        BucketList.objects.create(
            user=request.user,
            restaurant=restaurant
        )

    return redirect('restaurant_detail', pk=pk)


# 10. 맛집 트렌드 페이지
def restaurant_trend(request):
    # 버킷에 많이 담긴 맛집 TOP 10
    popular_restaurants = Restaurant.objects.prefetch_related('images').annotate(
        bucket_count=Count('bucketlist'),
        avg_rating=Avg('comments__rating')
    ).order_by('-bucket_count', '-avg_rating', '-id')[:10]

    # 지역별 맛집 제보 수
    location_trends_raw = Restaurant.objects.values('location').annotate(
        count=Count('id')
    ).order_by('-count')

    # 카테고리별 맛집 제보 수
    category_trends_raw = Restaurant.objects.values('category').annotate(
        count=Count('id')
    ).order_by('-count')

    # 코드값을 한글 이름으로 바꾸기
    location_dict = dict(Restaurant.LOCATION_CHOICES)

    # 예전에 저장된 지역 코드 보정
    location_dict.update({
        'SEO': '서울',
        'GN': '경남',
    })

    category_dict = dict(Restaurant.CATEGORY_CHOICES)

    # progress bar 비율 계산용
    max_location_count = location_trends_raw[0]['count'] if location_trends_raw else 1
    max_category_count = category_trends_raw[0]['count'] if category_trends_raw else 1

    location_trends = []
    for item in location_trends_raw:
        location_trends.append({
            'name': location_dict.get(item['location'], item['location']),
            'count': item['count'],
            'percent': int(item['count'] / max_location_count * 100),
        })

    category_trends = []
    for item in category_trends_raw:
        category_trends.append({
            'name': category_dict.get(item['category'], item['category']),
            'count': item['count'],
            'percent': int(item['count'] / max_category_count * 100),
        })

    total_restaurants = Restaurant.objects.count()
    total_buckets = BucketList.objects.count()

    return render(request, 'restaurants/restaurant_trend.html', {
        'popular_restaurants': popular_restaurants,
        'location_trends': location_trends,
        'category_trends': category_trends,
        'total_restaurants': total_restaurants,
        'total_buckets': total_buckets,
    })