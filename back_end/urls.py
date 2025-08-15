# project/urls.py
from django.contrib import admin
from django.urls import path, include
# from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # Your app's API endpoints
    path('api/', include('shop.urls')),

    # Authentication endpoints
    path("api/auth/", include("dj_rest_auth.urls")),  # login, logout, password reset
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),  # signup

    # Social login
    path("api/auth/social/", include("allauth.socialaccount.urls")),

    # Two-factor authentication
    # path("account/", include("two_factor.urls", "two_factor")),
    # path("account/", include((tf_urls, "two_factor"), namespace="two_factor")),
    # path("account/", include("two_factor.urls")),
    # path("account/", include("two_factor.urls")),
]
