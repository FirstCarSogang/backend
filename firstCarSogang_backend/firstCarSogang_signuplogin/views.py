from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from firstCarSogang_signuplogin.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token
import random
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .utils1 import generate_tokens, decode_token
from django.http import HttpResponse

# ===========================================================================================
class User_Registraion(View):
    def get(self, request):
        # 세션에서 이전 폼 데이터 가져오기
        form_data = request.session.get('form_data', {})
        return render(request, "registration.html", {'value': form_data})

    def post(self, request):
        # 첫 번째 단계에서의 요청인지 확인
        if 'name' in request.POST:
            # 첫 번째 단계 데이터 세션에 저장
            request.session['form_data'] = {
                'name': request.POST.get('name'),
                'username': request.POST.get('username'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'confirm_password': request.POST.get('confirm_password'),
                'kakaotalkID': request.POST.get('kakaotalkID')
            }
            return JsonResponse({'success': True})
        else:
            # 두 번째 단계에서의 요청인 경우 회원가입 처리
            form_data = request.session.get('form_data', {})
            form_data.update(request.POST)
            
            # 두 번째 단계에서 받은 데이터와 세션에 저장된 데이터를 함께 처리
            user = UserProfile(
                name=form_data.get('name'),
                email=form_data.get('email'),
                photo1=request.FILES.get('photo1'),
                photo2=request.FILES.get('photo2'),
                photo3=request.FILES.get('photo3'),
                username=form_data.get('username'),
                password=form_data.get('password'),
                kakaotalkID=form_data.get('kakaotalkID')
            )

            error_message = None
            

            # 세션 데이터 삭제
            del request.session['form_data']

            if not error_message:
                try:
                    user.save()
                    print("User saved successfully.")
                    return redirect("user_login")
                except Exception as e:
                    print("Error saving user:", str(e))
                    return redirect("user_login")
            else:
                print("Error message:", error_message)
                data = {
                    "error": error_message,
                    "value": form_data,
                }
                return render(request, "registration.html", data)
# ===========================================================================================

def clear_session_data(request):
    try:
        del request.session['form_data']
        return JsonResponse({'success': True})
    except KeyError:
        return JsonResponse({'success': False, 'error': 'Session data not found'}, status=400)


class send_otp1(View):
  
    def get(self, request):
        if request.method == 'GET':
            email = request.GET.get('email')
            if email:
                
                # OTP 생성
                otp = generate_unique_otp()
                request.session['otp'] = otp
                
                # 생성된 OTP 저장
                #EmailVerificationOTP.objects.create(email=email, otp=otp)

                # 생성된 OTP를 이메일로 전송
                subject = 'OTP Verification'
                message = f'Your OTP for registration is: {otp}'
                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                EmailMessage(subject, message, email_from, email_to).send()

                # 성공 응답 반환
                return JsonResponse({'success': True, 'message': 'OTP가 이메일로 전송되었습니다.'})
            else:
                return JsonResponse({'success': False, 'error_message': '이메일 주소가 제공되지 않았습니다.'})
        else:
            return JsonResponse({'success': False, 'error_message': '잘못된 요청 방식입니다.'})

class verify_otp(View):
    def get(self, request):
        if request.method == 'GET':
            otp = request.GET.get('otp')

            if not otp:
                return JsonResponse({'success': False, 'error_message': 'OTP가 제공되지 않았습니다.'})

            # 세션에서 저장된 OTP 확인
            session_otp = request.session.get('otp')
            if otp == session_otp:
                return JsonResponse({'success': True, 'message': 'OTP 인증이 완료되었습니다.'})
            else:
                return JsonResponse({'success': False, 'error_message': '유효하지 않은 OTP입니다.'})
        else:
            return JsonResponse({'success': False, 'error_message': '잘못된 요청 방식입니다.'})
    
    
# ===========================================================================================   

# ===========================================================================================
    
# ===========================================================================================
class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user = user)
            
            access_token, refresh_token = generate_tokens(user)
            response = redirect('home')
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})



# ===========================================================================================



@csrf_exempt
def forgot_password(request) :
    return render(request, 'forgot_password.html')

@csrf_exempt
def send_otp(request) :
    error_message = None
    otp = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    email = request.POST.get('email')
    user_email = UserProfile.objects.filter(email= email)
    if user_email :
        user = UserProfile.objects.get(email= email)
        user.otp = otp
        user.save()
        request.session['email'] = request.POST['email']
        html_message = "otp : " + "" + str(otp)
        subject = "비밀번호 초기화를 위한 otp"
        email_from = settings.EMAIL_HOST_USER
        email_to = [email]
        message = EmailMessage(subject, html_message, email_from, email_to)
        message.send()
        messages.success(request, '세인트이메일로 otp 전송했습니다.')
        return redirect('enter_otp')
    
        
    else :
        error_message = "Invalid Email please enter correct email"
        return render(request, 'forgot_password.html')
        
        
        
        
def enter_otp(request) :
    error_message = None
    if request.session.has_key('email') :
        email = request.session['email']
        user = UserProfile.objects.filter(email= email)
        for u in user :
            user_otp = u.otp
        if request.method == "POST" :
            otp = request.POST.get('otp')
            if not otp :
                error_message = "OTP 입력해주세요"
            elif not user_otp == otp :
                error_message = "제대로 된 otp입력해주세요"
            if not error_message :
                return redirect("password_reset")
        return render(request, 'enter_otp.html', {'error' : error_message})
    else :
        return render(request, "forgot_password.html", {'error' : error_message })




def password_reset(request) :
    error_message = None
    if 'email' in request.session:
        email = request.session['email']
        user = UserProfile.objects.get(email= email)
        if request.method == "POST" :
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            if not new_password :
                error_message = "새로운 비밀번호 입력"
            elif not confirm_new_password :
                 error_message = "새로운 확인 비밀번호 입력"
            elif new_password == user.password :
                error_message = "기존 비밀번호와 일치합니다. 새로운 비밀번호를 입력해주세요"
            elif not new_password == confirm_new_password:
                error_message = "비밀번호와 확인 비밀번호 동일하게 해주세요!!"
            if not error_message :
                user.password = new_password
                user.save()
                messages.success(request, "비밀번호 변경 성공")
                
                html_message = "비밀번호 변경 완료"
                subject = "첫차 서강 비밀번호 변경 완료"
                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                message = EmailMessage(subject, html_message, email_from, email_to)
                message.send()
                return redirect("user_login")
    return render(request, "password_reset.html", {'error' : error_message})

# ===========================================================================================
def home(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return HttpResponse("Unauthorized", status=401)

    user = decode_token(access_token)
    if user is not None:
        now = datetime.now()
        target = now.replace(hour=22, minute=0, second=0, microsecond=0)
        if now > target:
            target += timedelta(days=1) 

        countdown = target - now
        countdown_str = str(countdown).split('.')[0]  

        return render(request, 'home.html', {'user': user, 'countdown': countdown_str})
    else:
        return HttpResponse("Invalid token", status=401)

def toggle_ticket(request):
    if request.method == 'POST':
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        user = decode_token(access_token)
        if user is not None:
            user.useTicket = not user.useTicket
            user.save()
            return JsonResponse({'success': 'Ticket toggled successfully'})
        else:
            return JsonResponse({'error': 'Invalid token'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)