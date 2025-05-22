from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about', views.about, name='about'),
    path('videos', views.video_list, name='video_list'),]
# это часть urls.py тк все тоже самое (выполняется управление открытием нужных html страниц через поисковую строку 
# или параметром name в коде {% url "about" %}
