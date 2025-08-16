# back_end/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._has_phone_field = hasattr(self, 'fields') and 'phone' in self.fields

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['username'] = data.get('username', data.get('email', ''))
        return data

class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)
        
        if not user:
            raise serializers.ValidationError('No active account found with the given credentials')

        data = super().validate(attrs)
        return data