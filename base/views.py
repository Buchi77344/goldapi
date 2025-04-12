from django.shortcuts import render ,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.contrib.auth import authenticate, login
import random
from django.contrib import auth
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')


import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage, get_connection
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser  # Adjust the import to your project
from django.conf import settings 

import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage, get_connection
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser  # Import your CustomUser model properly

class SignupView(APIView):
    def post(self, request):
        try:
            # Get data from request
            first_name = request.data.get('first_name')
            email = request.data.get('email')
            password = request.data.get('password')

            # Validate input
            if not first_name or not email or not password:
                return Response(
                    {'error': 'All fields are required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user with email or username exists
            if CustomUser.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if CustomUser.objects.filter(username=email).exists():
                return Response(
                    {'error': 'Username already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Generate a random verification code
            code = random.randint(100000, 999999)

            # Create the user
            user = CustomUser.objects.create_user(
                username=email,
                first_name=first_name,
                email=email,
                password=password,
            )

            # Save additional fields if they exist in your model
            user.code = code
            user.user_type = 'buyer'
            user.save()

            # Send verification email
            try:
                connection = get_connection()  # Uses SMTP settings from settings.py
                email_message = EmailMessage(
                    subject='Your Verification Code',
                    body=f'Your verification code is: {code}',
                    from_email='from@example.com',  # Your sender email
                    to=[email],
                    connection=connection,
                )
                email_message.send(fail_silently=False)
            except Exception as e:
                # If email sending fails, delete the created user
                user.delete()
                return Response(
                    {'error': 'Failed to send verification email.', 'details': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': 'An unexpected error occurred.', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class VerifyEmail(APIView):
    def post(self, request):
        code = request.data.get('code')
        user = get_object_or_404(CustomUser, user=request.user)

        if code == user.code:
            return Response(
                {'success': 'Code matched successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Code does not match.'},
                status=status.HTTP_400_BAD_REQUEST
            )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)  # <-- Moved here
            return Response(
                {
                    "message": "Login successful",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )


class logoutapi(APIView):
    def post(self,request):
        auth.logout(request)
        return Response({"message":"logout successfully"},status=status.HTTP_200_OK)
    


# seller


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import SellerProfile

from django.db import transaction



class SellerRegistrationAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Passwords must match
        if password != confirm_password:
            return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create the User
                user = CustomUser.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    user_type='seller',   # Important! Assign as Seller
                )

                # Create Seller Profile
                seller_profile = SellerProfile.objects.create(
                    user=user,
                    company_name=data.get('company_name'),
                    company_reg_number=data.get('company_reg_number'),
                    phone_number=data.get('phone_number'),
                    country=data.get('country'),
                    website=data.get('website'),
                    address=data.get('address'),
                    company_certificate=data.get('company_certificate'),  # File
                    owner_id=data.get('owner_id'),                        # File
                    company_logo=data.get('company_logo'),                # File (optional)
                )

                return Response({'message': 'Seller registered successfully.'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# views.py

from rest_framework_simplejwt.tokens import RefreshToken

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

GOOGLE_CLIENT_ID = '492385262227-4pp9t7k2sa3rvmiu2hgbvs10i5ma1mpc.apps.googleusercontent.com'

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('id_token')

        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_CLIENT_ID)

            # ID token is valid
            email = idinfo.get('email')
            first_name = idinfo.get('given_name')
            last_name = idinfo.get('family_name')

            if not email:
                return Response({'error': 'Email not available'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists
            user, created = CustomUser.objects.get_or_create(email=email, defaults={
                'username': email.split('@')[0],  # Or some unique value
                'first_name': first_name or '',
                'last_name': last_name or '',
            })

            # Issue your tokens (using JWT here)
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })

        except ValueError:
            # Invalid token
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
