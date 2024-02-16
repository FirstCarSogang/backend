from django.shortcuts import render, redirect
from .models import Chatroom

def chatroom_view(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    users = chatroom.users.all()
    return render(request, 'chatroom.html', {'chatroom': chatroom, 'users': users})
