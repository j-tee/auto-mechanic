# back_end/admin.py
from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm

import shop
from .forms import AdminAuthenticationForm

admin.site.login_form = AdminAuthenticationForm
admin.site.login_template = 'admin/login.html'

# Register your models here.