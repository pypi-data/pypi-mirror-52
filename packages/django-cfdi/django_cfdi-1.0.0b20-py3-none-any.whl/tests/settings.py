import os

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    "cfdi",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "workflow.context_processors.custom_context",
            ]
        },
    }
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'tests',
    }
}



CFDI_ERROR_CALLBACK = "tests.cfdi_callbacks.error_callback"
CFDI_POST_TIMBRADO_CALLBACK = "tests.cfdi_callbacks.post_timbrado_callback"

CFDI_DFACTURE_AUTH = {
    "dev": {"usuario": "", "password": ""},
    "prod": {"usuario": "", "password": ""},
}
TEST_NO_CERTIFICADO = None
TEST_RFC = None
TEST_RAZON_SOCIAL = None
TEST_REGIMEN_FISCAL = None
TEST_CERTIFICADO = None
TEST_PEM = None

if os.path.exists("{}/local_settings.py".format(os.path.dirname(__file__))):
    from .local_settings import *