# back_end/admin.py
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
import shop
from .forms import AdminAuthenticationForm
from shop import models

admin.site.login_form = AdminAuthenticationForm
admin.site.login_template = 'admin/login.html'

# Register your models here.
User = get_user_model()
admin.site.unregister(User)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # If using custom user model without username
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


