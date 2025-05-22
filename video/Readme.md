 Выполнил Рудомётов Даниил Рооманович [ИКС-433]
 Web-приложение для видеохостинга и стриминга

Дисциплина: Веб-технологии  
Технологии: Django, PostgreSQL, Nginx, Redis, WebSocket (Channels), RTMP/HLS  



📌 Описание проекта
Проект представляет собой платформу для:
- Загрузки и хранения видео (аналог YouTube)
- Прямых трансляций с использованием RTMP/HLS



 🛠 Технологический стек
| Компонент   | Назначение                                                                |
|-------------|---------------------------------------------------------------------------|
| Django      | Backend-фреймворк для обработки запросов и работы с БД                    |
| PostgreSQL  | Реляционная СУБД для хранения данных пользователей и видео                |
| Nginx       | Веб-сервер + RTMP-сервер для трансляций                                   |
| Redis       | Кеширование и брокер сообщений для WebSocket                              |
| Channels    | Библиотека для работы с WebSocket (чат к трансляциям)                     |
| Gunicorn    | WSGI-сервер для запуска Django в продакшене                               |



 🏗 Архитектура Django
 1. Модели (`models.py`)
class Video(models.Model):
    title = models.CharField(max_length=200)  # Название видео
    video_file = models.FileField(upload_to='videos/')  # Путь к файлу

Назначение: Описывают структуру БД (таблицы, поля).


 2.Представления(views.py)
def video_list(request):
    videos = Video.objects.all()  # Получаем все видео из БД
    return render(request, 'videos/list.html', {'videos': videos})

Назначение: Обрабатывают HTTP-запросы и возвращают ответы.


3. URL-маршруты (urls.py)
path('videos/', views.video_list, name='video_list')

Назначение: Связывают URL с представлениями.


4. Шаблоны (templates/)
{% for video in videos %}
  <h2>{{ video.title }}</h2>
  <video src="{{ video.video_file.url }}"></video>
{% endfor %}
Назначение: Генерация HTML на сервере (Django Template Language).


5. Формы (forms.py)
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
Назначение: Валидация и обработка данных из HTML-форм.


🌐 Как работает стриминг?
RTMP-сервер (Nginx):

Принимает поток от OBS/Streamlabs.

Конвертирует в HLS для совместимости с браузерами.

nginx
rtmp {
    server {
        listen 1935;
        application live {
            live on;
            hls on;
            hls_path /tmp/hls;
        }
    }
}

### Краткое описание работы Django:
1. Запрос → URL → View → Модель → Шаблон – стандартный цикл обработки запроса.
2. ORM Django автоматически транслирует Python-код в SQL-запросы.
3. Шаблоны позволяют встраивать логику в HTML (аналогично PHP, но безопаснее).
4. Channels расширяет Django для работы с WebSocket и другими асинхронными протоколами.






