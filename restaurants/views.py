
from django.shortcuts import render, redirect
from .models import Restaurant
from .forms import RestaurantForm

def restaurant_list(request):
    all_res = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': all_res})

def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST,request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('restaurant_list') 
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/restaurant_create.html', {'form': form})