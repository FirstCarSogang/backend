from django.urls import path
from . import views

urlpatterns = [
    path('slowtrain/<int:ticket_number>/', views.ticket_detail, name='ticket_detail'),
]