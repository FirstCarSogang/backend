from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import NormalUser

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = NormalUser
        fields = ('username', 'password1', 'password2', 'email')
