from django.db import models
from django.contrib.auth.models import User
import uuid

class Stream(models.Model):
    """Модель для хранения стримов"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Модель пользователя
    title = models.CharField(max_length=100)  # Название стрима
    stream_key = models.CharField(max_length=50, unique=True)  # Уникальный ключ стрима
    is_active = models.BooleanField(default=False)  # Активен ли стрим
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f"{self.title} ({self.user.username})"  # Отображение в админке

    def get_stream_url(self):
        """Генерирует URL для HLS-потока"""
        return f'http://{HLS_SERVER}/hls/{self.stream_key}/index.m3u8'  # Генерация URL для потока 

    def get_rtmp_url(self):
        """Генерирует URL для RTMP-сервера"""
        return f'{RTMP_SERVER}/{self.stream_key}' # Генерация URL для сервера 

class Video(models.Model):
    """Модель для загруженных видео"""
    title = models.CharField(max_length=200)  # Название видео
    description = models.TextField(blank=True, null=True)  # Описание
    video_file = models.FileField(upload_to='videos/')  # Файл видео (сохраняется в media/videos/)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Кто загрузил
    upload_date = models.DateTimeField(auto_now_add=True)  # Дата загрузки

    def __str__(self):
        return self.title  # Отображение в админке

@classmethod
def create_for_user(cls, user):
    """Автоматическое создание стрима для нового пользователя"""
    stream_key = uuid.uuid4().hex[:12]  # Генерация случайного ключа
    return cls.objects.create(
        user=user,
        title=f'Stream {user.username}',
        stream_key=stream_key
    )
