from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import NormalUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = NormalUser
        fields = ['username', 'name', 'email', 'kakaotalkID', 'password1', 'photo1', 'photo2', 'photo3']

    def clean_studentID(self):
        student_id = self.cleaned_data['username']
        if len(str(student_id)) != 8:
            raise ValidationError("Student ID must be 8 digits long.")

        if NormalUser.objects.filter(username=student_id).exists():
            raise ValidationError("This student ID is already in use.")

        return student_id

    def clean_kakaotalkID(self):
        kakaotalk_id = self.cleaned_data['kakaotalkID']
        if NormalUser.objects.filter(kakaotalkID=kakaotalk_id).exists():
            raise ValidationError("This KakaoTalk ID is already in use.")

        return kakaotalk_id
