'''
Django settings for GRVTY project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
'''

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf import global_settings
from os.path import abspath, basename, dirname, join, normpath
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)

IN_DEVELOPMENT = True
USE_LOCAL_DATABASE = True
COMPRESS_ENABLED = True

MAIN_APP = True
CMS_APP = False
BILLING_APP = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# TODO: Change the secret key
SECRET_KEY = 'NOPE_CHUCK_TESTA!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = IN_DEVELOPMENT

# TODO: Change project name
PROJECT_NAME = 'GRVTY'

# TODO: ALLOWED HOSTS - Fill with the right credentials
ALLOWED_HOSTS = ['localhost', '127.0.0.1', ] if IN_DEVELOPMENT else []

# TODO: ADMINS - Fill with the right email
ADMINS = (('Chuck Testa', 'nope_chuck_testa@aol.com'), )

# ------------------------------ Application definition -----------------------
# TODO: NEW APPS - ADD INSTALLED
INSTALLED_APPS = list(filter(None, [
    'django.contrib.sites',  # Django-allauth
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'debug_toolbar',
    'rest_framework',
    'easy_thumbnails',

    'webpack_loader',  # Webpack

    'MainAPP',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
]))

SITE_ID = 1  # Django-allauth

# FIXME: ANTIPATTERN
if CMS_APP:
    from CMS.settings import INSTALLED_APPS as CMS_INSTALLED_APPS
    INSTALLED_APPS.extend(CMS_INSTALLED_APPS)
if BILLING_APP:
    from Billing.settings import INSTALLED_APPS as BILLING_INSTALLED_APPS
    INSTALLED_APPS.extend(BILLING_INSTALLED_APPS)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# FIXME: ANTIPATTERN
if CMS_APP:
    from CMS.settings import MIDDLEWARE_CLASSES as CMS_MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES.extend(CMS_MIDDLEWARE_CLASSES)
if BILLING_APP:
    from Billing.settings import MIDDLEWARE_CLASSES as BILLING_MIDDLEWARE_CLASSES
    MIDDLEWARE_CLASSES.extend(BILLING_MIDDLEWARE_CLASSES)


ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)

# ----------------- DEBUG TOOLBAR configuration -------------------------------

DEBUG_TOOLBAR_PATCH_SETTINGS = False

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = ['127.0.0.1', 'localhost', ]

# ----------------------------------- TEMPLATES -------------------------------

from django_jinja.builtins import DEFAULT_EXTENSIONS as DJJINJA_DEFAULT
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
                os.path.join(DJANGO_ROOT, 'templates'),
                os.path.join(DJANGO_ROOT, 'MainAPP/templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'extensions': DJJINJA_DEFAULT + [
                'compressor.contrib.jinja2ext.CompressorExtension',
                'webpack_loader.contrib.jinja2ext.WebpackExtension'
            ],
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(DJANGO_ROOT, 'allauth_templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': IN_DEVELOPMENT,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

# FIXME: ANTIPATTERN
# TODO: NEW APPS - ADD TEMPLATES
if CMS_APP:
    from CMS.settings import TEMPLATES as CMS_TEMPLATES
    TEMPLATES[0]['DIRS'].extend(CMS_TEMPLATES['DIRS'])
    TEMPLATES[0]['OPTIONS']['extensions'].extend(CMS_TEMPLATES['extensions'])
if BILLING_APP:
    from Billing.settings import TEMPLATES as BILLING_TEMPLATES
    TEMPLATES[0]['DIRS'].extend(BILLING_TEMPLATES['DIRS'])

WSGI_APPLICATION = '{}.wsgi.application'.format(PROJECT_NAME)

# ------------------------- COMPRESSOR configuration --------------------------

BABEL_LOCATION = '{}/node_modules/babel-cli/bin/babel.js'.format(DJANGO_ROOT)
COMPRESS_PRECOMPILERS = (
    (
       'text/jsx',
       BABEL_LOCATION + ' {infile} --out-file {outfile} --presets react'
    ),
    (
       'text/es6',
       BABEL_LOCATION + ' {infile} --out-file {outfile} --presets es2015'
    ),
    (
        'text/st1',
        BABEL_LOCATION + ' {infile} --out-file {outfile} --presets stage-1'
    ),
    (
        'text/st0',
        BABEL_LOCATION + ' {infile} --out-file {outfile} --presets stage-0'
    ),
)

# ------------------------ WEBPACK configuration ------------------------------

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(DJANGO_ROOT, 'webpack-stats.json'),
    }
}

# ------------------------------------ Database -------------------------------
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# TODO: Import the DATABASES setting from every other APP
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DJANGO_ROOT, 'db.sqlite3'),
    }
} if USE_LOCAL_DATABASE else {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # TODO: Change database engine
        'NAME': '{}'.format(PROJECT_NAME),
        'USER': 'django_{}'.format(PROJECT_NAME),
        'PASSWORD': 'NOPE_CHUCK_TESTA',  # TODO: Set new password
        'HOST': 'localhost'  # TODO: Change from localhost?
    }
}

# ---------------------- Password validation ----------------------------------
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

# ------------------------------ Internationalization -------------------------
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# -------------------- Static files (CSS, JavaScript, Images) -----------------
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/built/'

STATIC_ROOT = os.path.join(DJANGO_ROOT, 'built')

STATICFILES_DIRS = [
    os.path.join(DJANGO_ROOT, 'static'),
    os.path.join(DJANGO_ROOT, 'MainAPP/static'),
]

# FIXME: ANTIPATTERN
# TODO: NEW APPS - ADD STATIC
if CMS_APP:
    from CMS.settings import STATICFILES_DIRS as CMS_STATICFILES_DIRS
    STATICFILES_DIRS.extend(CMS_STATICFILES_DIRS)
if BILLING_APP:
    from Billing.settings import STATICFILES_DIRS as BILLING_STATICFILES_DIRS
    STATICFILES_DIRS.extend(BILLING_STATICFILES_DIRS)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# --------- Media files (those which can be modified by the end-users) --------
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(DJANGO_ROOT,  'media')

# -------------------- Custom configuration for login and avatars -------------

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/accounts/logout/'
AUTH_USER_MODEL = 'MainAPP.CustomUser'

ACCOUNT_LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SESSION_REMEMBER = True
SOCIALACCOUNT_QUERY_EMAIL = True

AUTHENTICATION_BACKENDS = [
    'MainAPP.architecture.backends.CustomUserModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
] + global_settings.AUTHENTICATION_BACKENDS

# -------------------- Django REST Framework configuration --------------------
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated avatars.
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        'rest_framework.permissions.IsAdminUser',
    ]
}

# ----------------------------WAGTAIL configuration ---------------------------

# TODO: Change Wagtail Admin name
WAGTAIL_SITE_NAME = 'GRVTY labs'

# TODO: Create and establish the templates
# PASSWORD_REQUIRED_TEMPLATE = 'myapp/password_required.html'
# WAGTAILSEARCH_RESULTS_TEMPLATE = 'tutorial/search_results.html'
# WAGTAILSEARCH_RESULTS_TEMPLATE_AJAX = 'tutorial/includes/search_listing.html'

# WAGTAILSEARCH_BACKENDS = {
#   'default': {
#     'BACKEND': 'wagtail.wagtailsearch.backends.elasticsearch',
#     'INDEX': 'MainAPP'
#   }
# }

WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = True
WAGTAIL_PASSWORD_RESET_ENABLED = True
TAGGIT_CASE_INSENSITIVE = True
WAGTAIL_ENABLE_UPDATE_CHECK = True

# TODO: Change Wagtail email and subject
EMAIL_SUBJECT_PREFIX = '[Wagtail] '
WAGTAILADMIN_NOTIFICATION_FROM_EMAIL = 'wagtail@myhost.io'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# -------------------- EASY_THUMBNAILS configuration --------------------------
THUMBNAIL_DEBUG = IN_DEVELOPMENT

THUMBNAIL_ALIASES = {
    '': {
        '50px': {'size': (50, 50), 'crop': True},
        '125px': {'size': (125, 125), 'crop': True},
        '150px': {'size': (150, 150), 'crop': True},
        '250px': {'size': (250, 250), 'crop': True},
        '350px': {'size': (350, 350), 'crop': True},
        '500px': {'size': (500, 500), 'crop': True},
    },
}
