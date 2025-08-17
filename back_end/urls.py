from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from back_end.views import CustomLoginView
from shop import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# ADMIN_LOGIN_URL = '/admin/login/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),

    #####################################
    # path('auth/', include('dj_rest_auth.urls')),
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ###########################################
    
    # Authentication endpoints
    path("api/auth/login/", CustomLoginView.as_view(), name="rest_login"),
    path("api/auth/", include("dj_rest_auth.urls")),
    #  path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    
    # Social login
    path('auth/social/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/social/github/', views.GitHubLogin.as_view(), name='github_login'),
    path('auth/social/facebook/', views.FacebookLogin.as_view(), name='facebook_login'),
    
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
        
    # Redirect allauth login to admin login
    path('accounts/login/', RedirectView.as_view(url=settings.ADMIN_LOGIN_URL, permanent=True)),
]