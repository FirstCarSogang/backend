from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import NormalUser
from django.contrib.auth.decorators import login_required

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username')
            user.save()
            return redirect('signup2')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def signup2(request):
    user_info = NormalUser.objects.last()
    if not user_info:
        return redirect('signup')

    if request.method == "POST":
        form = UserForm2(request.POST, request.FILES, instance=user_info)
        if form.is_valid():
            user_info = form.save(commit=False)
            if 'slow' in request.POST:
                user_info.sloworfast = 0
            elif 'fast' in request.POST:
                user_info.sloworfast = 1
            elif 'submit' in request.POST:
                return redirect('/')
            
            user_info.save()

    else:
        form = UserForm2(instance=user_info)

    return render(request, 'signup2.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Username and password are required fields.')    
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def mypage(request):
    user_profile = NormalUser.objects.get(username=request.user.username)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('mypage')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'mypage.html', {'user_profile': user_profile, 'form': form})
