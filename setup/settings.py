from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Lê do ambiente. Se não achar, usa uma chave insegura (fallback)
SECRET_KEY = os.getenv("SECRET_KEY", "chave-insegura-fallback")
# Lê do ambiente. Retorna 'True' se o valor for "True", senão False.
DEBUG = os.getenv("DEBUG", "False") == "True"
# Hosts permitidos
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
# O Render define a variável RENDER_EXTERNAL_HOSTNAME automaticamente
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

load_dotenv(BASE_DIR / ".env")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perfis',
    'empresas',
    'core_dashboard',
    'afiliados',
    'coletivos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'perfis.context_processors.perfil_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'

# Banco de dados
DATABASES = {
"default": dj_database_url.config(
default=os.getenv("DATABASE_URL"),
conn_max_age=600,
ssl_require=True, # Importante para Render
)
}
# Validação de Senhas

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'perfis.validators.ValidadorTamanhoMinimo',
        'OPTIONS': {
            'comprimento_minimo': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'perfis.validators.ValidadorComplexidadeSenha',
    },
]

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

# Arquivos CSS, JavaScript, Imagens
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Configurações de Login/Logout
LOGIN_REDIRECT_URL = '/pos-login/' #depois do login, nao vá direto para a home, vá primeiro para a minha logica
LOGOUT_REDIRECT_URL = 'login'

# Configurações de E-mail (Resend)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'resend' 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # Protegido via variável de ambiente
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'onboarding@resend.dev')