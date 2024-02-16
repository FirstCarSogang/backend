from .models import Ticket, Chatroom, Day1Question, AfterDay1Question
from django.contrib import admin
admin.site.register(Ticket)
admin.site.register(Chatroom)
admin.site.register(Day1Question)
admin.site.register(AfterDay1Question)