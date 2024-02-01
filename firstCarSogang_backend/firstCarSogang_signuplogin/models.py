from django.db import models
from django.contrib.auth.models import AbstractUser

class NormalUser(AbstractUser):
    studentID = models.IntegerField(unique=True, null=False, blank=False, verbose_name="서강대 학번")
    name = models.CharField(max_length=100, verbose_name="사용자명", null=False, blank=False)
    email = models.EmailField(max_length=100, verbose_name="서강대 E-mail", unique=True)
    kakaotalkID = models.CharField(max_length=100, verbose_name="카카오톡 ID", blank=True)
    photo1 = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    photo3 = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.studentID)
