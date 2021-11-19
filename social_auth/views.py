from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from register1.models import myUser
from django.contrib.auth import authenticate
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import GoogleSocialAuthSerializer,FacebookSocialAuthSerializer
# Create your views here.

@api_view(['POST',])
@permission_classes(())
def googleAuth(request):
    if request.method == 'POST':
        serializer = GoogleSocialAuthSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)
 

@api_view(['POST',])
@permission_classes(())
def facebookAuth(request):
    if request.method == 'POST':
        serializer = FacebookSocialAuthSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)