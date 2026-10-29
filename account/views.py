from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer
from .models import CustomUser, Profile
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'details': 'Your account has been registered successfully'}, status=status.HTTP_201_CREATED)

# "@permission_classes([IsAuthenticated])" Checks if the user is logged in, and have a valid token, if not, error 401 is sent
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = SignUpSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.username = data['username']
    user.email = data['email']
    user.set_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


def get_current_host(requset):
    protocol = requset.is_secure() and 'https' or 'http'
    host     = requset.get_host()
    return f"{protocol}://{host}/"


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(CustomUser, email=data['email'])
    token = get_random_string(40)
    expire_date = timezone.now() + timedelta(minutes=30)
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.reset_password_token = token
    profile.reset_password_expire = expire_date
    profile.save(update_fields=['reset_password_token', 'reset_password_expire'])

    host = get_current_host(request)
    link = f"{host}/api/reset_password/{token}/"
    body = f"Your password reset link is: {link}"
    # parameters: subject, message, from_email, recipient_list
    send_mail(
        "Password reset from Emarket",
        body,
        "Emarket@gmail.com",
        [data['email']]
    )
    return Response({"details": f"password reset sent to {data['email']}"})


@api_view(['POST'])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(CustomUser, profile__reset_password_token=token)
    token = get_random_string(40)
    profile, _ = Profile.objects.get_or_create(user=user)
    # if profile.reset_password_expire.replace(tzinfo=None) < datetime.now(): # type: ignore
    #     return Response({'error': 'Token is expired'}, status=status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Passwords are not the same!'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(data['password'])
    profile.reset_password_token = ""
    profile.reset_password_expire = None
    
    profile.save()
    user.save()

    
    return Response({"details": f"Password reset done!"})





