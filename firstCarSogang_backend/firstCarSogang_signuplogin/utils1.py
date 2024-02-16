import jwt
from django.conf import settings
from django.contrib.auth.models import User

def generate_tokens(user):
    access_token = jwt.encode({'username': user.username}, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    refresh_token = jwt.encode({'username': user.username}, settings.REFRESH_SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token, refresh_token

def decode_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        username = decoded['username']
        user = User.objects.get(username=username)
        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None