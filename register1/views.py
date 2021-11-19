from django.shortcuts import render
from rest_framework.serializers import Serializer
from .models import myUser
from .utils import Util

from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from .serializer import RegistrationSerializer, myUserSerializer,EmailVerificationSerializer, loginSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.generics import GenericAPIView

from .permission import SuperuserPermission

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from register1 import serializer

# Create your views here.

@api_view(['POST',])
@permission_classes(())
def reqistration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            my_user = serializer.save()
            data['response'] = "successfully registered a new user"
            data['username'] = my_user.username
            data['email'] = my_user.email
            token = Token.objects.get(user = my_user).key
            data['token'] = token
            # email verification
            current_site = get_current_site(request).domain
            relative_link = reverse('verifyEmail')
            absurl = 'http://' + current_site + relative_link + "?token="+str(token)
            email_body = 'Hi' + my_user.username + 'Use link below to verify your email \n' + absurl
            data_email = {'email_body': email_body, 'to_email': my_user.email, 'email_subject':'Verify your email'}
            Util.send_email(data_email)
        else:
            data = serializer.errors
        return Response(data)

# token_param_config = 

@api_view(['GET'])
@permission_classes(())
def verifyEmail(request): 
    token = request.GET.get('token')
    user = myUser.objects.get(auth_token = token)
    if user.is_active == False:
        user.is_active = True
        user.save()
        return Response({'Response': 'Account activated'}, status = status.HTTP_200_OK)
    return Response({'Response': 'Account already activated'}, status = status.HTTP_200_OK)



@api_view(['POST',])
@permission_classes(())
def login(request):
    if request.method == 'POST':
        serializer = loginSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((SuperuserPermission,)) #used custom permisssions
def myUsers(request):
    myUsers = myUser.objects.all()
    serializer = myUserSerializer(myUsers, many = True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser,])
def getUserById(request, pk):
    user = myUser.objects.get(id=pk)
    serializer = myUserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getUserProfile(request):
    user = myUser.objects.get(email = request.user)
    serializer = myUserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def userUpdate(request):
    user = myUser.objects.get(email = request.user)

    if request.method == 'PUT':
        serializer = myUserSerializer(instance = user,data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            user.set_password(serializer.data.get("password"))
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def userDelete(request):
    user = myUser.objects.get(email = request.user)
    if request.method == 'DELETE':
        user.delete()
        return Response('Item succsesfully delete!')