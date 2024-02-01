from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserForm

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method =="POST":
        form = UserForm (request.POST)
        if form.is_valid():
            form.save()
            studentID=form.cleaned_data.get('studentID')
            name=form.cleaned_data.get('name')
            email=form.cleaned_data.get('email')
            kakaotalkID =form.cleaned_data.get('kakaotalkID')
            password=form.cleaned_data.get('password1')
            photo1 =form.cleaned_data.get('photo1')
            photo2 =form.cleaned_data.get('photo2')
            photo3 =form.cleaned_data.get('photo3')
            user=authenticate(username=studentID,password=password)
            login(request,user)
    else:
        form=UserForm()
    return render(request,'signup.html', {'form':form})