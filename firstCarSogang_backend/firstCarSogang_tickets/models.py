from django.db import models
from firstCarSogang_signuplogin.models import NormalUser
from random import shuffle

class Ticket(models.Model):
    ticketNumber = models.IntegerField(verbose_name="티켓 번호")
    progressingDay = models.IntegerField(verbose_name="진행중인 날짜")
    isAnswered = models.BooleanField(verbose_name="답변 여부", default=False)
    choose = models.BooleanField(verbose_name="선택 여부", default=False)
    withWhom = models.CharField(max_length=100, verbose_name="대상")
    day1_question = models.OneToOneField('Day1Question', on_delete=models.CASCADE)
    after_day1_question = models.OneToOneField('AfterDay1Question', on_delete=models.CASCADE, related_name='ticket')
    users = models.ManyToManyField(NormalUser, related_name='tickets', verbose_name="여기에 포함된 사용자들")

    def __str__(self):
        return f"{self.ticketNumber}: {self.progressingDay} 일째 대화"

    def initiate_conversation(self):
        users_with_tickets=self.users.filter(userTicket=True)
        if users_with_tickets.count()<2:
            return
        users_list=list(users_with_tickets)
        shuffle(users_list)
        chatroom= Chatroom.objects.create()
        chatroom.users.set(users_list)
        if self.progressingDay == 1:
            self.send_question_message(users_list[0], self.day1_question.question)
            self.send_question_message(users_list[1], self.day1_question.question)
        else:
            self.send_question_message(users_list[0], self.after_day1_question.question)
            self.send_question_message(users_list[1], self.after_day1_question.question)
        self.choose = True 
    
        
class Chatroom(models.Model):
    users=models.ManyToManyField(NormalUser,related_name="chatrooms")
class Day1Question(models.Model):
    question = models.CharField(max_length=1000, verbose_name="질문")
    placeholder = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000, verbose_name="대답", blank=True, null=True)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, related_name='daily_question')

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
    answer = models.CharField(verbose_name="주관식 답변", blank=True, null=True, max_length=1000)
    answer2=models.IntegerField(default=1)
    def __str__(self):
        return f"AfterDay1Question {self.question_id}: {self.question}"