import os
import dj_database_url

# === 1. Configuración Básica ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# IMPORTANTE: En producción, cambia esto por False y usa variables de entorno
SECRET_KEY = '-_&+lsebec(whhw!%n@ww&1j=4-^j_if9x8$q778+99oz&!ms2'
DEBUG = False

# Permitimos todo por ahora para que no te de lata al probar
ALLOWED_HOSTS = ['*']


# === 2. Aplicaciones Instaladas ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # <--- Solo una vez, ¡super importante!
    
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    
    # Tu app (asegúrate que el nombre coincida con tu carpeta)
    'app_movil_escolar_api',
]

# === 3. Middleware (El orden importa muchísimo) ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',      # CORS va antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app_movil_escolar_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app_movil_escolar_api.wsgi.application'


# === 4. Base de Datos ===
# Nota: En PythonAnywhere usualmente usas MySQL, pero aquí dejo tu config
# Si falla la conexión después, revisaremos esto.
#DATABASES = {
#   'default': dj_database_url.config(
#      default='postgresql://postgres:postgres@localhost:5432/mysite',
#     conn_max_age=600
    #)
#}

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://neondb_owner:npg_Q5OKcz0oywZf@ep-floral-art-adzkwfjo-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
        conn_max_age=600
    )
}

# === 5. Validadores de Contraseña ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# === 6. Internacionalización ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Configuración de WhiteNoise para producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# === 8. Configuración de REST Framework ===
REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'app_movil_escolar_api.models.BearerTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}


# === 9. Configuración CORS ===
CORS_ALLOWED_ORIGINS = [
    "https://proyecto-final-webapp-oficial.vercel.app",
    "http://localhost:4200",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True