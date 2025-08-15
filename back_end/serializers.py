from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    """
    Extends the default RegisterSerializer to include only email & password,
    handle username automatically, and fix _has_phone_field error.
    """
    username = serializers.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add missing attribute to prevent errors in allauth
        self._has_phone_field = hasattr(self, 'fields') and 'phone' in self.fields

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        validated_data = dict(getattr(self, 'validated_data', {}) or {})
        # Use username if provided, otherwise fallback to email
        data['username'] = validated_data.get('username', data.get('email', ''))
        return data