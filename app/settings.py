"""
Django's settings for app project.
"""

import os
from pathlib import Path

# импортируем наши данные из env файла
from dotenv import load_dotenv

# загружаем данные
load_dotenv()

# BASE_DIR = C:\Users\dyako\PycharmProjects\webapps\songix_backend
# базовый путь к проекту (в котором лежит manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# Меняется на False, когда выкатывается на основной сервер
# (чтобы пользователю не отображалась отладочная информация на странице)
DEBUG = eval(os.getenv('DEBUG'))

# * - указывает, что приложение может работать на любых хостах
# или можно указать свои, например, mysite.com
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',' or ', ')

# Application definition
# Здесь определяем наши приложения (отдельные логические блоки, которые нам необходимы для проекта)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',

    # наши приложения
    'users',  # для работы с пользователями

    # подключаем полнотекстовый поиск django
    'django.contrib.postgres',

    # приложение для дополнительной отладки django
    'debug_toolbar',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # доп
    # отключаем стандартный csrf
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # добавляем дополнительный инструмент для отладки
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # подключаем наш кастомный csrf для обработки CSRF ошибок
    'app.middleware.CustomCsrfMiddleware',
]

# файл urls.py, где указаны все url-адреса нашего приложения
ROOT_URLCONF = 'app.urls'

# шаблонизатор для отрисовки html-страниц
# DIRS - где дополнительно искать шаблоны, указываем папку templates в корне
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# какой протокол работы используем (wsgi or asgi)
WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# NAME - имя БД
# USER - имя пользователя; HOST - хост, на котором работает БД (IP-адрес); PORT - порт IP-адреса
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('NAME_DB'),
        'USER': os.getenv('USER_DB'),
        'PASSWORD': os.getenv('PASSWORD_DB'),
        'HOST': os.getenv('IP_DB'),
        'PORT': os.getenv('PORT_DB'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# валидаторы паролей (минимальная длина, верхний и нижний регистр и тд)
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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# на каком языке работает приложение django, на каком языке будет отображаться admin-панель,
# оповещения для пользователей и тд
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# какой префикс будет добавлен, при получении статических файлов (css, js и тд), в браузере будет отображаться
# следующий примерный путь: /staticfiles/deps/css/style.css
STATIC_URL = 'staticfiles/'

# для развертывания (collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# какой префикс будет добавлен, при получении медиа-файлов
MEDIA_URL = 'media/'

# где django будет искать медиа-файлы (в папке media)
MEDIA_ROOT = BASE_DIR / 'media'

# где будет работать дополнительный инструмент для отладки
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# автоинкремент (+1) id для каждой новой записи в БД в каждом приложении
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# указываем какую модель использовать вместо auth_user (нашу дополненную модель)
AUTH_USER_MODEL = 'users.User'

# путь к нашему представлению login (url-адрес), чтобы переопределить страницу "Not Found" у модуля
# login_required на нашу страницу авторизации
LOGIN_URL = '/user/login/'

# сервер будет принимать запросы из любых источников, независимо от их доменного имени
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Укажите ваш клиентский домен
    "https://www.songix.ru",  # Укажите другие домены, если они нужны
    "https://songix.ru",  # Укажите другие домены, если они нужны
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

CORS_ALLOW_CREDENTIALS = True

# ограничивать доступ конкретными доменами
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3000',
# ]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'app.exceptions.custom_exception_handler',
}
