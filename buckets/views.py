from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from restaurants.models import Restaurant
from .models import BucketList


@login_required(login_url='accounts:login')
def add_bucket(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    bucket, created = BucketList.objects.get_or_create(
        user=request.user,
        restaurant=restaurant
    )

    if created:
        messages.success(request, f'"{restaurant.name}"이(가) 내 FooKet에 담겼습니다! 🧺')
    else:
        messages.info(request, f'"{restaurant.name}"은(는) 이미 FooKet에 들어있어요. ✨')

    return redirect('buckets:list')


@login_required(login_url='accounts:login')
def bucket_list(request):
    my_buckets = BucketList.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'buckets/bucket_list.html', {'my_buckets': my_buckets})


@login_required(login_url='accounts:login')
def delete_bucket(request, bucket_id):
    bucket = get_object_or_404(BucketList, pk=bucket_id, user=request.user)
    bucket.delete()
    messages.warning(request, 'FooKet에서 삭제되었습니다.')
    return redirect('buckets:list')


@login_required(login_url='accounts:login')
def update_bucket_memo(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    bucket = get_object_or_404(
        BucketList,
        user=request.user,
        restaurant=restaurant
    )

    if request.method == 'POST':
        bucket.memo = request.POST.get('memo', '')
        bucket.save()
        messages.success(request, '메모가 저장되었습니다.')

    return redirect('restaurant_detail', pk=restaurant.id)