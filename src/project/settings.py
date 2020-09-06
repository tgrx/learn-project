import os
from itertools import chain
from pathlib import Path

import dj_database_url
import sentry_sdk
from django.urls import reverse_lazy
from dynaconf import settings as _ds
from sentry_sdk.integrations.django import DjangoIntegration

PROJECT_DIR = Path(__file__).parent
BASE_DIR = PROJECT_DIR.parent
REPO_DIR = BASE_DIR.parent

SECRET_KEY = _ds.SECRET_KEY

DEBUG = _ds.DEBUG

if not DEBUG:
    sentry_sdk.init(
        dsn=_ds.SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

INTERNAL_IPS = ["127.0.0.1"]
INTERNAL_HOSTS = ["localhost"]
ALLOWED_HOSTS = list(chain(_ds.ALLOWED_HOSTS or [], INTERNAL_IPS, INTERNAL_HOSTS))

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "applications.blog.apps.BlogConfig",
    "applications.hello.apps.HelloConfig",
    "applications.onboarding.apps.OnboardingConfig",
    "applications.pr.apps.PrConfig",
    "applications.projects.apps.ProjectsConfig",
    "applications.stats.apps.StatsConfig",
    "applications.target.apps.TargetConfig",
    "applications.theme.apps.ThemeConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates",],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "applications.theme.contextprocessors.theme",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

database_url = _ds.DATABASE_URL
if _ds.ENV_FOR_DYNACONF == "heroku":
    database_url = os.getenv("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.parse(database_url),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/s/"
STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]
STATIC_ROOT = REPO_DIR / ".static"
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = reverse_lazy("onboarding:sign-in")
LOGIN_REDIRECT_URL = reverse_lazy("projects:all")

AWS_ACCESS_KEY_ID = _ds.AWS_ACCESS_KEY_ID
AWS_QUERYSTRING_AUTH = False
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_AVATARS_LOCATION = _ds.AWS_S3_AVATARS_LOCATION
AWS_S3_OBJECT_PARAMETERS = {"ACL": "public-read"}
AWS_S3_REGION_NAME = _ds.AWS_S3_REGION_NAME
AWS_SECRET_ACCESS_KEY = _ds.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = _ds.AWS_STORAGE_BUCKET_NAME
