import os
import dj_database_url  # Importado para manejar la conexión de Render/PostgreSQL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mantén la clave secreta en variables de entorno en producción (¡SÚPER IMPORTANTE!)
SECRET_KEY = os.environ.get('SECRET_KEY', '-_&+lsebec(whhw!%n@ww&1j=4-^j_if9x8$q778+99oz&!ms2')

DEBUG = True # en desarrollo
# En Render, DEBUG se desactiva cuando ALLOWED_HOSTS no está vacío
if os.environ.get('RENDER'):
    DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".render.com"] # Añadido dominio de Render

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters', # necesarios para los filtros de DRF
    'rest_framework',
    'rest_framework.authtoken', # conserva soporte de tokens de DRF
    'corsheaders', # librería CORS actualizada
    'app_movil_escolar_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- NUEVO: Para servir archivos estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de CORS: define orígenes permitidos y quita CORS_ORIGIN_ALLOW_ALL
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
]
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'app_movil_escolar_api.urls'


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = "/static/"
# --- Configuración de Archivos Estáticos para Render/Whitenoise ---
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# -----------------------------------------------------------------


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

# <---------------- NUEVA CONFIGURACIÓN DE BASE DE DATOS PARA POSTGRESQL EN RENDER ----------------->
DATABASES = {
    'default': dj_database_url.config(
        # dj_database_url buscará la variable de entorno DATABASE_URL en Render
        conn_max_age=600,
        ssl_require=True # Requerido por la mayoría de los hosts de PostgreSQL como NeonDB o Render
    )
}
# <------------------------------------------------------------------------------------------------>


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

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