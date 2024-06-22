from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


class LoginView(APIView):

    def post(self,request):
        try:
            username = request.data.get('id')
            password = request.data.get('password')

            user = authenticate(password=password,username=username)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            else:
                return Response({'status':False,'message':'Invalid credentials'},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':False,'message':'Something unexpected occurred'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class CreateView(APIView):
    
    def post(self,request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'message':'User created successfully'},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'status':False,'errors':serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status':False,'message':'Something unexpected occurred'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



