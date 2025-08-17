# back_end/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = serializers.CharField(required=False)
        self.fields['email'] = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        "User account is disabled.")

                # refresh = self.get_token(user)
                refresh = RefreshToken.for_user(user)
                data = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'pk': user.pk,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }
                return data

        raise serializers.ValidationError(
            "Unable to log in with provided credentials.")
class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    "Unable to log in with provided credentials.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")

            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                "Must include 'email' and 'password'.")

        return attrs

# clas
class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            # Check if email exists using EmailAddress model
            if email and EmailAddress.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError(
                    "A user is already registered with this e-mail address.")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                "The two password fields didn't match.")
        return data

    def get_cleaned_data(self):
        validated_data = getattr(self, 'validated_data', {}) or {}
        return {
            'email': validated_data.get('email', ''),
            'password1': validated_data.get('password1', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        return user
