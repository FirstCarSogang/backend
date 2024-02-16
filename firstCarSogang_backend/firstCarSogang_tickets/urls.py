from django.urls import path
from . import views

urlpatterns = [
    path('chatroom/<int:chatroom_id>/', views.chatroom_view, name='chatroom'),
]
