from django.urls import path
from firstCarSogang_signuplogin.views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', UserLoginView.as_view(), name='user_login'),
    path('user_registration/', User_Registraion.as_view(),name='user_registration'),
    path('forgot_password', forgot_password, name='forgot_password'),
    path('send_otp', send_otp, name='send_otp'),
    path('enter_otp', enter_otp, name='enter_otp'),
    path('password_reset', password_reset, name='password_reset'),
    path('send_otp1/', send_otp1.as_view(), name='send_otp1'),
    path('verify_otp/', verify_otp.as_view(), name='verify_otp'),
    path('home', home, name='home'),  
    path('clear_session_data/', clear_session_data, name='clear_session_data'),

]