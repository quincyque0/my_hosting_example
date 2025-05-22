# Web-приложение для видеохостинга и стриминга

**Выполнил:** Рудомётов Даниил Рооманович [ИКС-433]  
**Дисциплина:** Веб-технологии  

---

## 📌 Описание проекта
Платформа для:
- 📹 Загрузки и хранения видео (аналог YouTube)
- 🔴 Прямых трансляций с использованием RTMP/HLS
- 💬 Реализации чата через WebSocket (опционально)

---

## 🛠 Технологический стек
| Компонент       | Назначение                                                                 |
|-----------------|---------------------------------------------------------------------------|
| **Django**      | Backend-фреймворк для обработки запросов и работы с БД                    |
| **PostgreSQL**  | Реляционная СУБД для хранения данных                                      |
| **Nginx**       | Веб-сервер + RTMP-сервер для трансляций                                   |
| **Redis**       | Кеширование и брокер сообщений для WebSocket                              |
| **Channels**    | Поддержка WebSocket                                                       |
| **Gunicorn**    | WSGI-сервер для продакшена                                               |

---

## 🏗 Архитектура Django

### 1. Модели (`models.py`)
```python
class Video(models.Model):
    title = models.CharField(max_length=200)  # Название видео
    video_file = models.FileField(upload_to='videos/')  # Путь к файлу
Назначение: Описание структуры БД (таблицы и связи)
```
2. Представления (views.py)
```python
def video_list(request):
    videos = Video.objects.all()  # Получаем все видео из БД
    return render(request, 'videos/list.html', {'videos': videos})
Назначение: Логика обработки HTTP-запросов
```
3. Маршрутизация (urls.py)
```python
path('videos/', views.video_list, name='video_list')
Назначение: Связь URL-адресов с представлениями
```
4. Шаблоны (templates/)
```html
{% for video in videos %}
  <div class="video">
    <h2>{{ video.title }}</h2>
    <video controls src="{{ video.video_file.url }}"></video>
  </div>
{% endfor %}
```
Назначение: Генерация HTML с данными

5. Формы (forms.py)
```python
class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
```
Назначение: Валидация и обработка данных форм

🌐 Стриминг-механизм
Работа RTMP/HLS
```nginx
rtmp {
    server {
        listen 1935;
        application live {
            live on;
            hls on;
            hls_path /tmp/hls;
            hls_fragment 3s;
        }
    }
}
```
Процесс:

OBS отправляет поток на RTMP-сервер (Nginx)

Nginx конвертирует в HLS-формат

Браузер получает адаптивный поток через .m3u8 плейлист
### Краткое описание работы Django:
1. Запрос → URL → View → Модель → Шаблон – стандартный цикл обработки запроса.
2. ORM Django автоматически транслирует Python-код в SQL-запросы.
3. Шаблоны позволяют встраивать логику в HTML (аналогично PHP, но безопаснее).
4. Channels расширяет Django для работы с WebSocket и другими асинхронными протоколами.

