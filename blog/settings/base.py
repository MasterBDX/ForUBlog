import os

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# Email host settings

DEFAULT_FROM_EMAIL = 'masterbdxteam@gmail.com'


MANAGERS = (('masterbdx', 'masterbdxteam@gmail.com'),)
ADMINS = MANAGERS


DEFAULT_ACTIVATION_DAYS = 7


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party packs
    'rest_framework',
    'rest_framework.authtoken',
    'tinymce',
    'crispy_forms',
    'storages',
    'django_social_share',
    'django.contrib.sitemaps',
    'debug_toolbar',
    'django_hosts',


    # my apps
    'main',
    'accounts',
    'marketing',
    'posts',
    'comments',
    'search',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'blog.middleware.LangSessionMiddletware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware'
]

ROOT_URLCONF = 'blog.urls'
ROOT_HOSTCONF = 'blog.hosts'
DEFAULT_HOST = 'www'



AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = 'main:home'
LOGIN_URL = '/account/login/'

# crispy pack we use to style forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# =============


VALID_IMAGE_WIDTH = 800
VALID_IMAGE_HEIGHT = 450

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 700,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft aligncenter alignright |
             alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.categories_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'accounts.passwords.validators.IsAsciiValidator'},
    {'NAME': 'accounts.passwords.validators.MinimumLengthValidator'},
    {'NAME': 'accounts.passwords.validators.NumberValidator'},
    # {'NAME': 'accounts.passwords.validators.UppercaseValidator', },
    # {'NAME': 'accounts.passwords.validators.LowercaseValidator', },
    {'NAME': 'accounts.passwords.validators.SymbolValidator', },
]


SITE_ID = 1

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
