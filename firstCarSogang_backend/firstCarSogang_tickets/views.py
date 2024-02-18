from django.shortcuts import render, redirect
from .models import Chatroom,Day1Question,Ticket
from django.http import JsonResponse

def chatroom_view(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    users = chatroom.users.all()
    return render(request, 'chatroom.html', {'chatroom': chatroom, 'users': users})

def slow_train(request):
    username=request.user.username

    day1_questions=Ticket.objects.filter(users__username=username)
    
    data = {
        'day1_questions': [
            {
                'id': question.id,
                'question': question.question,
                'placeholder': question.placeholder,
            }
            for question in day1_questions
        ]
    }
    return JsonResponse(data)