from django.db import models
from firstCarSogang_signuplogin.models import NormalUser

class Ticket(models.Model):
    ticketNumber = models.IntegerField(verbose_name="티켓 번호")
    progressingDay = models.IntegerField(verbose_name="진행중인 날짜")
    isAnswered = models.BooleanField(verbose_name="답변 여부", default=False)
    choose = models.BooleanField(verbose_name="선택 여부", default=False)
    withWhom = models.CharField(max_length=100, verbose_name="대상")
    day1_question = models.OneToOneField('Day1Question', on_delete=models.CASCADE, related_name='ticket_related')
    after_day1_question = models.OneToOneField('AfterDay1Question', on_delete=models.CASCADE, related_name='ticket_related')
    users = models.ManyToManyField(NormalUser, related_name='tickets', verbose_name="여기에 포함된 사용자들")

    def __str__(self):
        return f"Ticket {self.ticketNumber} with {self.withWhom}"

class Day1Question(models.Model):
    question = models.CharField(max_length=1000, verbose_name="질문")
    placeholder = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, verbose_name="대답", blank=True, null=True)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='signuplogin_daily_questions')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='day_questions')

    def __str__(self):
        return f"Question: {self.question} - User: {self.user}"

class AfterDay1Question(models.Model):
    question_id = models.IntegerField(verbose_name="질문 ID", unique=True)
    question = models.CharField(max_length=1000, verbose_name="질문1")
    placeholder = models.CharField(max_length=1000)
    multipleChoiceAnswer1 = models.CharField(max_length=1000, verbose_name="객관식 답변1")
    multipleChoiceAnswer2 = models.CharField(max_length=1000, verbose_name="객관식 답변2")
    multipleChoiceAnswer3 = models.CharField(max_length=1000, verbose_name="객관식 답변3")
    multipleChoiceAnswer4 = models.CharField(max_length=1000, verbose_name="객관식 답변4")
    multipleChoiceAnswer5 = models.CharField(max_length=1000, verbose_name="객관식 답변5")
    answer = models.CharField(verbose_name="주관식 답변", max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"AfterDay1Question {self.question_id}: {self.question}"
