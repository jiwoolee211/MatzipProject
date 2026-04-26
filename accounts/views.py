from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_check = request.POST.get('password_check')

        if not username or not password or not password_check:
            return render(request, 'accounts/signup.html', {
                'error': '모든 칸을 입력해주세요.'
            })

        if password != password_check:
            return render(request, 'accounts/signup.html', {
                'error': '비밀번호가 일치하지 않습니다.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {
                'error': '이미 존재하는 아이디입니다.'
            })

        User.objects.create_user(
            username=username,
            password=password
        )
        return redirect('accounts:login')

    return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')   
        else:
            return render(request, 'accounts/login.html', {
                'error': '아이디 또는 비밀번호가 올바르지 않습니다.'
            })

    return render(request, 'accounts/login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')
