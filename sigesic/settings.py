"""
Sistema Integral de Gestión para las Industrias y el Comercio (SIGESIC)

Copyleft (@) 2015 CENDITEL nodo Mérida - https://sigesic.cenditel.gob.ve/trac/
"""
## @package sigesic.settings
#
# Configuración de funcionalidades y parámetros del sistema
# @author Generated by 'django-admin startproject' using Django 1.8.
# @author Ing. Roldan Vargas (rvargas at cenditel.gob.ve)
# @author <a href='http://www.cenditel.gob.ve'>Centro Nacional de Desarrollo e Investigación en Tecnologías Libres
# (CENDITEL) nodo Mérida - Venezuela</a>
# @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>GNU Public License versión 2 (GPLv2)</a>
# @version 2.0

# Django settings for sigesic project.
# Generated by 'django-admin startproject' using Django 1.9.
# For more information on this file, see https://docs.djangoproject.com/en/1.9/topics/settings/
# For the full list of settings and their values, see https://docs.djangoproject.com/en/1.9/ref/settings/
from __future__ import unicode_literals

import os

from .database_config import DATABASES_CONFIG

## Directorio base desde donde se encuentra ejecutando la aplicación
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

## Número de versión de la aplicación
VERSION = '3.0.0'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_9jt8ll@#+3&#u$w^&c%_e^wp1^t$r21)1706fvow-k(c)=2id'

## Identifica si el sistema se encuentra en modo de desarrollo (True) o en modo producción (False)
DEBUG = True

## Identifica a los servidores permitidos que atienden las peticiones del sistema
ALLOWED_HOSTS = ['localhost']

## Identifica a los administradores del sistema
ADMINS = [
    ('Ing. Roldan Vargas', 'rvargas@cenditel.gob.ve'),
]

## Listado de aplicaciones base del sistema
PREREQ_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
]

if DEBUG:
    ## Aplicaciones requeridas para entornos de desarrollo
    PREREQ_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]

    ## Configuracion de parametros de django-debug-toolbar
    JQUERY_URL = ''

## Listado de aplicaciones del projecto
PROJECT_APPS = [
    'base',
    'usuario',
    'unidad_economica.directorio',
    'unidad_economica',
    'unidad_economica.informacion_mercantil',
    'unidad_economica.sub_unidad_economica',
    'unidad_economica.maquinaria_equipo',
    'unidad_economica.bienes_prod_comer',
    'unidad_economica.insumo_proveedor',
    'unidad_economica.servicios',
    'unidad_economica.coyuntura',
    #Aplicación de carga masiva debe colocarse después de las aplicaciones de producción
    'carga_masiva',
]

## Listado de aplicaciones cargadas por el sistema
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE_CLASSES += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

## Configuración de las URL del sistema
ROOT_URLCONF = 'sigesic.urls'

## Directorio en donde se encuentran las plantillas en el root de la aplicación
ROOT_TEMPLATES = os.path.join(BASE_DIR, "templates")

## Directorio en donde se encuentran las plantillas del módulo base
BASE_TEMPLATES = os.path.join(BASE_DIR, "base/templates")

## Directorio en donde se encuentran las plantillas del módulo de usuarios
USERS_TEMPLATES = os.path.join(BASE_DIR, "usuario/templates")

## Directorio en donde se encuentran las plantillas del módulo de Unidad Económica
UNIDAD_ECONOMICA_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/templates")

## Directorio en donde se encuentran las plantillas del módulo Información Mercantil
INFORMACION_MERCANTIL_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/informacion_mercantil/templates")

## Directorio en donde se encuentran las plantillas del módulo de Sub Unidad Económica
SUB_UNIDAD_ECONOMICA_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/sub_unidad_economica/templates")

## Directorio en donde se encuentran las plantillas del módulo maquinaria_equipos
MAQUINARIA_EQUIPO_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/maquinaria_equipos/templates")

## Directorio en donde se encuentran las plantillas del módulo de bienes producidos y comercializados
BIENES_PROD_COMER_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/bienes_prod_comer/templates")

## Directorio en donde se encuentran las plantillas del módulo de bienes producidos y comercializados
INSUMOS_PROVEEDORES_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/insumo_proveedor/templates")

## Directorio en donde se encuentran las plantillas del módulo de bienes producidos y comercializados
SERVICIOS_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/servicios/templates")

## Directorio en donde se encuentran las plantillas del módulo de coyuntura
COYUNTURA_TEMPLATES = os.path.join(BASE_DIR, "unidad_economica/coyuntura/templates")

## Directorio en donde se encuentran los templates de carga masiva
CARGA_MASIVA_TEMPLATES = os.path.join(BASE_DIR, "carga_masiva/templates")

CARGA_MASIVA_FILES = os.path.join(BASE_DIR, "static/cm")



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_TEMPLATES, BASE_TEMPLATES, USERS_TEMPLATES, UNIDAD_ECONOMICA_TEMPLATES,
            INFORMACION_MERCANTIL_TEMPLATES, SUB_UNIDAD_ECONOMICA_TEMPLATES, MAQUINARIA_EQUIPO_TEMPLATES,
            BIENES_PROD_COMER_TEMPLATES, INSUMOS_PROVEEDORES_TEMPLATES, SERVICIOS_TEMPLATES, COYUNTURA_TEMPLATES,
            CARGA_MASIVA_TEMPLATES,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                "django.template.context_processors.tz",
            ],
        },
    },
]

## Configuración para el wsgi de la aplicación
WSGI_APPLICATION = 'sigesic.wsgi.application'


## Configuración de la(s) base(s) de dato(s) del sistema
DATABASES = DATABASES_CONFIG


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

## Configuración para las validaciones de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

## Configuración del código del lenguaje a utilizar por defecto
LANGUAGE_CODE = 'es-ve'

## Configuración para el nombre de localización por defecto
LOCALE_NAME = 'es'

## Configuración para la zona horaria por defecto
TIME_ZONE = 'America/Caracas'

## Determina si se emplea la internacionalización I18N
USE_I18N = True

## Determina si se emplea la internacionalización L10N
USE_L10N = True

## Determina si se emplea la zona horaria
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

## Configuración de la raíz donde se encuentran los archivos estaticos del sistema (para entornos en producción)
STATIC_ROOT = ''

## Configuración de la url que atenderá las peticiones de los archivos estáticos del sistema
STATIC_URL = '/static/'

## Configuración de los directorios en donde se encuentran los archivos estáticos
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
    #os.path.join(BASE_DIR, 'tmp/'),
)

## URL de acceso al sistema
LOGIN_URL = "/login"

## URL de salida del sistema
LOGOUT_URL = "/logout"

## configuración que permite obtener la ruta en donde se encuentran las traducciones de la aplicación a otros lenguajes
LOCALE_PATHS = [
    #os.path.join(BASE_DIR, 'locale'),
]

## Registro de mensajes al usuario
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Configuración de variables para el envío de correo electrónico
## Nombre del Servidor de correo SMTP
EMAIL_HOST = 'localhost'
## Puerto del Servidor de correo SMTP
EMAIL_PORT = 25
## Dirección de correo electrónico de quien envía
EMAIL_FROM = 'sigesic@cenditel.gob.ve'

## Registro de vitácoras de errores (logs)
LOGS_PATH = '/home/cenditel/Proyectos/sigesic_v2/log/sigesic'

## Configuración de los niveles de vitácoras (logs) a registrar
LOGGING = dict(version=1, disable_existing_loggers=True, formatters={
    'std': {
        'format': '%(asctime)s %(levelname)-8s [modulo: %(module)s, funcion: %(funcName)s, linea: %(lineno)d]. %(message)s',
    }
}, handlers={
    'null': {
        'level': 'DEBUG',
        'class': 'logging.NullHandler'
    },
    'base': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'std',
        'filename': os.path.join(LOGS_PATH, 'base.log'),
        'when': 'w6',
        'interval': 1,
        'backupCount': 52
    },
    'usuario': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'std',
        'filename': os.path.join(LOGS_PATH, 'usuario.log'),
        'when': 'w6',
        'interval': 1,
        'backupCount': 52
    },
    'ue': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'std',
        'filename': os.path.join(LOGS_PATH, 'ue.log'),
        'when': 'w6',
        'interval': 1,
        'backupCount': 52
    },
    'carga_masiva': {
        'class': 'logging.handlers.TimedRotatingFileHandler',
        'level': 'DEBUG',
        'formatter': 'std',
        'filename': os.path.join(LOGS_PATH, 'carga_masiva.log'),
        'when': 'w6',
        'interval': 1,
        'backupCount': 52
    },
}, loggers={
    'root': {
        'level': 'DEBUG',
        'handlers': ['usuario']
    },
    'base': {
        'level': 'DEBUG',
        'handlers': ['base'],
        'qualname': 'base'
    },
    'usuario': {
        'level': 'DEBUG',
        'handlers': ['usuario'],
        'qualname': 'usuario'
    },
    'ue': {
        'level': 'DEBUG',
        'handlers': ['ue'],
        'qualname': 'ue'
    },
    'carga_masiva': {
        'level': 'DEBUG',
        'handlers': ['carga_masiva'],
        'qualname': 'carga_masiva'
    },
    'django.request': {
        'handlers': ['null'],
        'level': 'ERROR',
        'propagate': False,
    }
})

# Configuración del CAPTCHA
## Ruta en donde se encuentra el diccionario de palabras a utilizar en la generación del captcha
CAPTCHA_WORDS_DICTIONARY = os.path.join(BASE_DIR, "static/dictionaries/captcha-es.txt")
## Establece el tipo de captcha a generar. Se establece a la extraccion de palabras a partir de un diccionario
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'
## Longitud de carácteres a mostrar en la imagen del captcha
CAPTCHA_LENGTH = 6
## Longitud de carácteres máxima permitida para extraer del diccionario
CAPTCHA_DICTIONARY_MAX_LENGTH = 6
## Longitud de carácteres mínima permitida para extraer del diccionario
CAPTCHA_DICTIONARY_MIN_LENGTH = 4
## Color de fondo para la imagen del captcha
CAPTCHA_BACKGROUND_COLOR = '#337AB7'
## Color de la fuente para la imagen del captcha
CAPTCHA_FOREGROUND_COLOR = '#FFF'

if DEBUG:
    ## Elimina la imagen de ruido en el fondo del captcha cuando la aplicacion se encuentra en modo desarrollo
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)

    ## Tiempo de expiración del captcha en entornos de desarrollo, representado en minutos
    CAPTCHA_TIMEOUT = 1440 # 24 horas

    ## Configura el backend para el envío de correo electrónico para mostrarlo en consola, solo en entorno de desarrollo
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
