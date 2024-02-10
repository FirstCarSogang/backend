from celery import shared_task
from django.utils import timezone
from .models import Ticket

@shared_task
def match_users():
    current_time = timezone.now().time()
    if current_time.hour == 22 and current_time.minute == 0:
        for ticket in Ticket.objects.all():
            ticket.initiate_conversation()

@shared_task
def give_questions():
    current_time = timezone.now().time()
    if current_time.hour == 0 and current_time.minute == 0:
        for ticket in Ticket.objects.all():
            ticket.upload_questions()