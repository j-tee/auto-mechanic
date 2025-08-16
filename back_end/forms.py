# back_end/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class AdminAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Bypass email verification check for admin
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )