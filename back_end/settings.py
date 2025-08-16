from pathlib import Path
from socket import gethostname
from dotenv import load_dotenv
import os
from datetime import timedelta

# ====== Base Configuration ======
BASE_DIR = Path(__file__).resolve().parent.parent

# ====== Environment Detection ======
hostname = gethostname().lower()
ENVIRONMENT = "development"

if "staging" in hostname:
    ENVIRONMENT = "staging"
elif "prod" in hostname or "server" in hostname:
    ENVIRONMENT = "production"

# Manual override
ENVIRONMENT = os.getenv("DJANGO_ENV", ENVIRONMENT)

# Load environment variables
dotenv_path = BASE_DIR / f".env.{ENVIRONMENT}"
load_dotenv(dotenv_path)
print(f"[INFO] Environment: {ENVIRONMENT} — loaded {dotenv_path}")

# ====== Core Settings ======
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []
ROOT_URLCONF = 'back_end.urls'
WSGI_APPLICATION = 'back_end.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ====== Application Definition ======
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Third-party apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'corsheaders',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django_otp',
    'two_factor',
    'django_filters',
    
    # Local apps
    'back_end',
    'shop',
]

# Social providers
SOCIAL_PROVIDERS = [
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',
]
INSTALLED_APPS += SOCIAL_PROVIDERS

# ====== Middleware ======
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ====== Database ======
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

# ====== Authentication & Authorization ======
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Allauth settings
SITE_ID = 1
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_SIGNUP_FIELDS = ["email", "password1", "password2"]

# Conditional email verification
ACCOUNT_EMAIL_VERIFICATION = "mandatory" if ENVIRONMENT == "production" else "none"

# Admin login
ADMIN_LOGIN_PATH = 'admin/login/'
LOGIN_URL = f'/{ADMIN_LOGIN_PATH}'
LOGIN_REDIRECT_URL = '/admin/'

# ====== REST Framework & JWT ======
REST_USE_JWT = True
REST_AUTH = {
    'LOGIN_SERIALIZER': 'back_end.serializers.CustomLoginSerializer',
    'REGISTER_SERIALIZER': 'back_end.serializers.CustomRegisterSerializer',
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.JWTSerializer',
}
ACCOUNT_ADAPTER = "back_end.adapters.CustomAccountAdapter"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
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
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ====== Internationalization ======
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ====== Static Files ======
STATIC_URL = 'static/'

# ====== Templates ======
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ====== Email Configuration ======
if DEBUG or ENVIRONMENT == "development":
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
    EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "true").lower() == "true"
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# ====== CORS Configuration ======
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") or [
    "http://localhost:3000", 
    "http://127.0.0.1:3000"
]

# ====== Security Settings ======
if not DEBUG:
    # Add production security settings here
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True