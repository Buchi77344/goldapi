from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth import authenticate, login

from django.contrib import auth

# Create your views here.
def index(request):
    return render(request, 'index.html')

class signupview(APIView):
    def post(self, request):
        first_name =request.data.get('first_name')
        email =request.data.get('email')
        password =request.data.get('password')
        username =request.data.get('username')

        if not  first_name or not email or not password:
            return Response({
                'error': 'All fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({
                'error':'email already exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(username=username).exists():
            return Response({
                'error':'username already exist'
            }, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create_user(username=email, first_name=first_name,email=email,password=password)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh':str(refresh),
                'access': str(refresh.access_token)
            } , status= status.HTTP_201_CREATED
        )


class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        refresh = RefreshToken.for_user(user)  # Change username=email to work with email-based login
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful",
                 'refresh':str(refresh),
                'access': str(refresh.access_token)
                             }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        

class logoutapi(APIView):
    def post(self,request):
        auth.logout(request)
        return Response({"message":"logout successfully"},status=status.HTTP_200_OK)