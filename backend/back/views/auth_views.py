# Authentication-related views


from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from google.auth.transport import requests
from google.oauth2 import id_token


# ------------------ Google Login ------------------
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), "YOUR_GOOGLE_CLIENT_ID")
            email = id_info.get("email")
            name = id_info.get("name")

            user, _ = User.objects.get_or_create(email=email, defaults={"username": name})
            auth_token, _ = Token.objects.get_or_create(user=user)

            return Response({"token": auth_token.key}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# ------------------ Traditional Registration ------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already in use."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)


# ------------------ Traditional Login ------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("identifier")  # Can be username or email
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"message": "Username/Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=identifier).first() or User.objects.filter(email=identifier).first()
        if not user or not authenticate(username=user.username, password=password):
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "is_superuser": user.is_superuser,
            "message": "Login successful"
        }, status=status.HTTP_200_OK)
