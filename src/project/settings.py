import os
from pathlib import Path

import dj_database_url

PROJECT_DIR = Path(__file__).parent
BASE_DIR = PROJECT_DIR.parent
REPO_DIR = BASE_DIR.parent

SECRET_KEY = "1"

DEBUG = 1

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "tms-learn-project.herokuapp.com",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "applications.hello.apps.HelloConfig",
    "applications.projects.apps.ProjectsConfig",
    "applications.stats.apps.StatsConfig",
    "applications.target.apps.TargetConfig",
    "applications.theme.apps.ThemeConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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

development_database_url = "postgresql://alex:alex@localhost:5432/z01"
database_url = os.getenv("DATABASE_URL", development_database_url)
database_params = dj_database_url.parse(database_url)

DATABASES = {
    "default": database_params,
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

STATIC_URL = "/static/"
