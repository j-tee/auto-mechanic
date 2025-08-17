# back_end/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from back_end.serializers import CustomRegisterSerializer, EmailTokenObtainPairSerializer
from dj_rest_auth.registration.views import RegisterView

# Removed duplicate EmailTokenObtainPairView class to resolve name conflict.

from dj_rest_auth.views import LoginView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import logging
logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
    
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)

        refresh = RefreshToken.for_user(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'pk': user.pk,
                'email': user.email,
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)


class EmailTokenObtainPairView(APIView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
