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
     'rest_framework_simplejwt', 
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rest_framework.authtoken',
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
     'back_end.authentication.EmailBackend',
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

# REST_AUTH_SERIALIZERS = {
#     "LOGIN_SERIALIZER": "dj_rest_auth.serializers.LoginSerializer",
#     "USER_DETAILS_SERIALIZER": "dj_rest_auth.serializers.UserDetailsSerializer",
# }
# Allauth settings
SITE_ID = 1
# Tell allauth what your username field is (if using default Django user model)
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
# Define which fields are required at signup
ACCOUNT_SIGNUP_FIELDS = ["username", "email", "password1", "password2"]

# Define how users can log in
ACCOUNT_LOGIN_METHODS = ["email"]  # or just ["email"] if you prefer
ACCOUNT_EMAIL_VERIFICATION = "mandatory" if ENVIRONMENT == "production" else "none"

# ====== REST Framework & JWT ======
# REST_USE_JWT = True

# Configure dj_rest_auth to use JWT properly
REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    'JWT_AUTH_COOKIE': 'access_token',
    'JWT_AUTH_REFRESH_COOKIE': 'refresh_token',
    # 'TOKEN_MODEL': None,
    'TOKEN_SERIALIZER': 'back_end.serializers.EmailTokenObtainPairSerializer',
    'LOGIN_SERIALIZER': 'back_end.serializers.CustomLoginSerializer',
    'REGISTER_SERIALIZER': 'back_end.serializers.CustomRegisterSerializer',
    # 'JWT_SERIALIZER': None,  # Disable default JWT serializer
    
}
ACCOUNT_ADAPTER = "back_end.adapters.CustomAccountAdapter"

# Configure REST framework}
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
    'UPDATE_LAST_LOGIN': True,  # Add this
    'ALGORITHM': 'HS256',  # Add this
    'SIGNING_KEY': SECRET_KEY,  # Add this
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JSON_ENCODER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',  # Add this
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',  # Add this
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',  # Add this
}

# ====== Internationalization ======
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ====== Static Files ======
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # For production
STATICFILES_DIRS = [BASE_DIR / 'static']  # For development

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

# ====== Admin Fix ======
# Use the standard Django admin login
# ACCOUNT_LOGOUT_ON_GET = True  # Fixes allauth logout issues
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' if DEBUG else 'https'
# ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/admin/'

# Explicitly set admin login path
ADMIN_LOGIN_URL = '/admin/login/'
LOGIN_URL = ADMIN_LOGIN_URL
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/'

# from rest_framework_simplejwt.tokens import RefreshToken
import warnings
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers"
)
