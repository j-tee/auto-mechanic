# back_end/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

User = get_user_model()
class CustomAccountAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        return User()
    
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.email = data.get('email')
        user.username = data.get('email')  # Set username to email
        
        if 'password1' in data:
            user.password = make_password(data['password1'])
        else:
            user.set_unusable_password()
        
        if commit:
            user.save()
        return user