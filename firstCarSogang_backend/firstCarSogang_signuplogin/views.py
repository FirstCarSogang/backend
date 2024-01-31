from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import EmailAuthenticationForm 

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
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'] 
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})