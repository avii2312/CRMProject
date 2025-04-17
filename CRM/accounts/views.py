from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import datetime

def landing(request):
    return render(request, 'landingpage.html')

# Signup view with email verification using JWT
class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.'})
        # Create user as inactive until email verification
        user = User.objects.create_user(username=username, email=email, password=password, is_active=False)
        # Generate a verification token (expires in 24 hours)
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        # Build the verification URL
        verification_url = request.build_absolute_uri(reverse('email_verify') + f'?token={token}')
        subject = 'Verify your email'
        message = f'Hi {username}, please verify your email by clicking on the link: {verification_url}'
        from_email = settings.DEFAULT_FROM_EMAIL  # Ensure you have this defined in settings
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return render(request, 'signup.html', {'message': 'Please check your email to verify your account.'})

# Email verification view
class EmailVerifyView(View):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            user = User.objects.get(id=user_id)
            if not user.is_active:
                user.is_active = True
                user.save()
                return render(request, 'email_verified.html', {'message': 'Email verified successfully. You can now log in.'})
            else:
                return render(request, 'email_verified.html', {'message': 'Email is already verified.'})
        except jwt.ExpiredSignatureError:
            return render(request, 'email_verified.html', {'error': 'Verification link expired.'})
        except jwt.DecodeError:
            return render(request, 'email_verified.html', {'error': 'Invalid verification token.'})

# Custom Login View that issues JWT tokens upon successful authentication
class CustomLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                return render(request, 'login.html', {'error': 'Account not active. Please verify your email.'})
            login(request, user)
            # Generate JWT tokens using SimpleJWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            # Store tokens in the session (or consider cookies if more appropriate)
            request.session['access_token'] = access_token
            request.session['refresh_token'] = refresh_token
            return redirect('client_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

# Custom Logout View that clears session tokens
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        request.session.pop('access_token', None)
        request.session.pop('refresh_token', None)
        return redirect('login')

# Home view to display login success and token info
class HomeView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        return render(request, 'home.html', {'access_token': access_token})

# Protected API endpoint that requires a valid JWT token
class ProtectedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"message": "This is protected data accessible only with a valid JWT."}
        return Response(data)








# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.views import View
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
#
#
# class CustomLoginView(View):
#     def get(self, request):
#         return render(request, 'login.html')
#
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)
#             request.session['access_token'] = access_token
#             request.session['refresh_token'] = refresh_token
#             return redirect('home')  # Redirect to a home page
#         else:
#             return render(request, 'login.html', {'error': 'Invalid credentials'})
#
# # Custom Logout View that clears the session tokens
# class CustomLogoutView(View):
#     def get(self, request):
#         logout(request)
#         request.session.pop('access_token', None)
#         request.session.pop('refresh_token', None)
#         return redirect('login')
#
# # Home view to display login success and token information
# class HomeView(View):
#     def get(self, request):
#         access_token = request.session.get('access_token')
#         return render(request, 'home.html', {'access_token': access_token})
#
# # Protected API endpoint that requires a valid JWT token
# class ProtectedDataView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         data = {"message": "This is protected data accessible only with a valid JWT."}
#         return Response(data)
