from pathlib import Path
from socket import gethostname
from dotenv import load_dotenv
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
hostname = gethostname()

# Auto-detect environment based on hostname
if "staging" in hostname.lower():
    ENVIRONMENT = "staging"
elif "prod" in hostname.lower() or "server" in hostname.lower():
    ENVIRONMENT = "production"
else:
    ENVIRONMENT = "development"

# Allow manual override
ENVIRONMENT = os.getenv("DJANGO_ENV", ENVIRONMENT)

# Load environment variables
dotenv_path = BASE_DIR / f".env.{ENVIRONMENT}"
load_dotenv(dotenv_path)

print(f"[INFO] Environment: {ENVIRONMENT} — loaded {dotenv_path}")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(
    ",") if os.getenv("ALLOWED_HOSTS") else []

# Applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Sites framework for allauth
    'django.contrib.sites',

    # Allauth (Email & Social login)
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',

    # DRF + Auth
    'rest_framework',
    'corsheaders',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',
    # Removed "dj_rest_auth.social_serializers" — not a valid app, this caused app loading issues

    # 2FA
    "django_otp",
    "django_otp.plugins.otp_totp",
    "two_factor",

    # Your apps
    'back_end',
    'shop',

    # Filters
    'django_filters',
]

SITE_ID = 1
REST_USE_JWT = True

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.JWTSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'back_end.serializers.CustomRegisterSerializer',
}
ACCOUNT_ADAPTER = "back_end.adapters.CustomAccountAdapter"

# DRF & JWT
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Change to IsAuthenticated in production
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Auth backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Ensure CORS is applied before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_otp.middleware.OTPMiddleware',  # Required for 2FA
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'back_end.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'back_end.wsgi.application'

# Database — left exactly as you had it
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth account settings (new format)
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # still valid



# Email backend
if ENVIRONMENT == "development":
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# CORS for React frontend
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == ['']:
    CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
