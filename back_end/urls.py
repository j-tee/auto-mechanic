# project/urls.py
from django.contrib import admin
from django.urls import path, include
# from two_factor.urls import urlpatterns as tf_urls
from shop import views  # Adjust 'shop' to the correct app name if needed
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from back_end.views import CustomTokenObtainPairView

urlpatterns = [
    # Admin with proper login
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('shop.urls')),
    
    # Authentication endpoints (API only)
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    
    # Social login
    path('auth/social/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/social/github/', views.GitHubLogin.as_view(), name='github_login'),
    path('auth/social/facebook/', views.FacebookLogin.as_view(), name='facebook_login'),
    
    # JWT endpoints
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
# urlpatterns = [
#     path('admin/', admin.site.urls),

#     # Your app's API endpoints
#     path('api/', include('shop.urls')),

#     # Authentication endpoints
#     path("api/auth/", include("dj_rest_auth.urls")),  # login, logout, password reset
#     path("api/auth/registration/", include("dj_rest_auth.registration.urls")),  # signup

#     # Updated JWT endpoints
#     path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

#     # Social login
#     path("api/auth/social/", include("allauth.socialaccount.urls")),
#      path('auth/social/google/', views.GoogleLogin.as_view(), name='google_login'),
#     path('auth/social/github/', views.GitHubLogin.as_view(), name='github_login'),
#     path('auth/social/facebook/', views.FacebookLogin.as_view(), name='facebook_login'),
#     # path('api/auth/social/', include('dj_rest_auth.social_urls')),
#  # JWT endpoints
#     # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     # Two-factor authentication
#     # path("account/", include("two_factor.urls", "two_factor")),
#     # path("account/", include((tf_urls, "two_factor"), namespace="two_factor")),
#     # path("account/", include("two_factor.urls")),
#     # path("account/", include("two_factor.urls")),
# ]
