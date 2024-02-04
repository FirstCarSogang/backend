from django.db import models
from django.contrib.auth.models import AbstractUser

def user_directory_path(instance, filename):
    return 'user/photos/{0}/{1}'.format(instance.username, filename)

class NormalUser(AbstractUser):
    username = models.CharField(unique=True, null=True, blank=True, max_length=10,verbose_name="서강대 학번")
    name = models.CharField(max_length=100, verbose_name="사용자명", null=False, blank=False)
    email = models.EmailField(max_length=100, verbose_name="서강대 E-mail", unique=True)
    kakaotalkID = models.CharField(max_length=100, verbose_name="카카오톡 ID", blank=True)
    photo1 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    photo2 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    photo3 = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    sloworfast=models.BooleanField(default=True)

    def __str__(self):
        return str(self.username)

class Day1Question(models.Model):
    question=models.CharField(verbose_name="질문", max_length=1000)
    answer=models.CharField(verbose_name="대답", max_length=1000)
