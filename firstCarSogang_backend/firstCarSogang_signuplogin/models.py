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
    ticketCount=models.IntegerField()

    def __str__(self):
        return str(self.username)

from django.db import models

class Ticket(models.Model):
    ticketNumber = models.IntegerField(verbose_name="티켓 번호")
    progressingDay = models.IntegerField(verbose_name="진행중인 날짜")
    isAnswered = models.BooleanField(verbose_name="답변 여부", default=False)
    choose = models.BooleanField(verbose_name="선택 여부", default=False)
    withWhom = models.CharField(max_length=100, verbose_name="대상")
    day1_question = models.OneToOneField('Day1Question', on_delete=models.CASCADE, related_name='ticket')
    after_day1_question = models.OneToOneField('AfterDay1Question', on_delete=models.CASCADE, related_name='ticket')

    def __str__(self):
        return f"Ticket {self.ticketNumber} with {self.withWhom}"

class Day1Question(models.Model):
    question = models.CharField(max_length=1000, verbose_name="질문")
    placeholder = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, verbose_name="대답", blank=True, null=True)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='daily_questions')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='day_questions')

    def __str__(self):
        return f"Question: {self.question} - User: {self.user}"

from django.db import models
class AfterDay1Question(models.Model):
    question_id = models.IntegerField(verbose_name="질문 ID", unique=True)
    question = models.CharField(max_length=1000, verbose_name="질문1")
    placeholder = models.CharField(max_length=1000)
    multipleChoiceAnswer1 = models.CharField(max_length=1000, verbose_name="객관식 답변1")
    multipleChoiceAnswer2 = models.CharField(max_length=1000, verbose_name="객관식 답변2")
    multipleChoiceAnswer3 = models.CharField(max_length=1000, verbose_name="객관식 답변3")
    multipleChoiceAnswer4 = models.CharField(max_length=1000, verbose_name="객관식 답변4")
    multipleChoiceAnswer5 = models.CharField(max_length=1000, verbose_name="객관식 답변5")
    answer = models.CharField(verbose_name="주관식 답변", blank=True, null=True)

    def __str__(self):
        return f"AfterDay1Question {self.question_id}: {self.question}"