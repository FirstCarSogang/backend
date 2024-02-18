from django.urls import path
from .views import chatroom_view,slow_train 

urlpatterns = [
    path('chatroom/<int:chatroom_id>/', chatroom_view, name='chatroom'),
    path('slowtrain/', slow_train,name="slow_train"),
    
]
