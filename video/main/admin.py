from django.contrib import admin
from .models import Video

admin.site.register(Video) #ну это просто чтобы в админке можно было создавать и удалять видео
