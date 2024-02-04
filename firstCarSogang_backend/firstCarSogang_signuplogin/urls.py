from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('signup/1', views.signup, name='signup'),
    path('signup/2', views.signup2, name='signup2'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]
