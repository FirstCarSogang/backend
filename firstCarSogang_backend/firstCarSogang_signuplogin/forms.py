from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserForm(UserCreationForm):
    username = forms.IntegerField(label="학번")
    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'email', 'kakaotalkID', 'password1']
    def clean_username(self):
        username = self.cleaned_data['username']
        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("This student ID is already in use.")        
        return username
    
    def clean_kakaotalkID(self):
        kakaotalk_id = self.cleaned_data['kakaotalkID']
        if UserProfile.objects.filter(kakaotalkID=kakaotalk_id).exists():
            raise ValidationError("This KakaoTalk ID is already in use.")
        return kakaotalk_id

class UserForm2(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['photo1', 'photo2', 'photo3']
    
class LoginForm(forms.Form):
    username=forms.CharField(label="username")
    password = forms.CharField(widget=forms.PasswordInput, label="password")

    def clean_username(self):
        username=str(self.cleaned_data.get('username'))
        if not username.isdigit():
            raise ValidationError('Username must contain only numbers.')
        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("This student ID is already in use.")        
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields=['photo1','photo2','photo3','sloworfast']
        
