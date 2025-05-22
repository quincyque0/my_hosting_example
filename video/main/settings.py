# этот скрипт я немогу полность показать тк эта информация поможет злоумышеникам получить контроль над сайтом

import os
from pathlib import Path

# Базовые пути проекта
BASE_DIR = Path(__file__).resolve().parent.parent  # Корневая директория проекта

# Настройки аутентификации
LOGIN_URL = '/accounts/login/'  # URL для входа
LOGIN_REDIRECT_URL = 'stream_view'  # Перенаправление после входа
LOGOUT_REDIRECT_URL = '/'  # Перенаправление после выхода

# Безопасность
SECRET_KEY = 'django-insecure-...'  # Ключ для шифрования (По понятнмы причинам пуст)
DEBUG = False  # Режим отладки (False для продакшена)
ALLOWED_HOSTS = ['Разрешенные хосты']  # Разрешенные хосты (для теста — '*', в продакшене указываются домены домен)

# Приложения
INSTALLED_APPS = [
    'rest_framework',  # Django REST Framework
    'main',  # Ваше основное приложение
    'channels',  # Для WebSocket
    # Стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    ...
]

# Настройки Channels (WebSocket)
ASGI_APPLICATION = 'main.asgi.application'  # Указывает на ASGI-приложение
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",  # Хранение WebSocket-сессий в Redis
        "CONFIG": {
            "hosts": [("redis-host", 6379)],  # Адрес Redis-сервера
        },
    },
}

# База данных (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'namedb',  # Имя БД
        'USER': 'username',  # Пользователь
        'PASSWORD': 'password',  # Пароль (не храните в коде!)
        'HOST': 'localhost',  # Хост
        'PORT': '5432',  # Порт
    }
}

# Настройки медиафайлов
MEDIA_URL = '/media/'  # URL для медиа
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Директория для загрузки файлов

# Настройки электронной почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ваш_email@yandex.ru'  # Замените на реальный email
EMAIL_HOST_PASSWORD = 'ваш_пароль'  # Пароль от почты

# Настройки RTMP/HLS
RTMP_SERVER = 'rtmp://localhost/live'  # Адрес RTMP-сервера
HLS_SERVER = 'http://localhost/hls'  # Адрес HLS-сервера

# HTTPS-настройки (для продакшена у меня пока не используются значения FALSE)
SECURE_HSTS_SECONDS = 31536000  # Включить HSTS
SECURE_SSL_REDIRECT = True  # Перенаправлять HTTP → HTTPS
SESSION_COOKIE_SECURE = True  # Защищенные куки
CSRF_COOKIE_SECURE = True  # Защита от CSRF
