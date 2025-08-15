# adapters.py
from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Adapter to override the default behavior and avoid _has_phone_field error.
    Handles email-only registration and saves user properly.
    """
    def save_user(self, request, user, form, commit=True):
        # Fix: Add missing attribute if it doesn't exist
        if not hasattr(form, '_has_phone_field'):
            form._has_phone_field = hasattr(form, 'fields') and 'phone' in form.fields
        
        # Proceed with default saving process
        user = super().save_user(request, user, form, commit=False)
        data = form.cleaned_data
        
        # Ensure email is properly set
        user.email = data.get('email')
        
        # Set username with email fallback
        user.username = data.get('username') or data.get('email')
        
        if commit:
            user.save()
        return user