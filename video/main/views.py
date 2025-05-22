from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Stream
from .models import Video
from .forms import VideoUploadForm
from django.contrib import messages
import uuid
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# ======================
# Основные страницы
# ======================

def index(request):
    """Главная страница приложения"""
    return render(request, 'main/home.html')

def about(request):
    """Страница 'О нас'"""
    return render(request, 'about.html')

# ======================
# Функционал стриминга
# ======================

def stream(request):
    """Страница просмотра стримов"""
    return render(request, 'main/stream.html')

@csrf_exempt
def stream_auth(request):
    """
    Аутентификация стрима (API endpoint)
    POST-параметры:
    - key: stream key для аутентификации
    """
    if request.method == 'POST':
        key = request.POST.get('key', '')
        try:
            stream = Stream.objects.get(stream_key=key)
            stream.is_active = True
            stream.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Stream.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid stream key'}, status=403)
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def stream_end(request):
    """
    Завершение стрима (API endpoint)
    POST-параметры:
    - key: stream key для завершения
    """
    if request.method == 'POST':
        key = request.POST.get('key', '')
        try:
            stream = Stream.objects.get(stream_key=key)
            stream.is_active = False
            stream.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Stream.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def stream_view(request):
    """
    Страница управления стримом для авторизованных пользователей
    Автоматически создает stream key если его нет
    """
    stream, created = Stream.objects.get_or_create(
        user=request.user,
        defaults={
            'title': f'Stream {request.user.username}',
            'stream_key': uuid.uuid4().hex[:12] 
        }
    )
    
    context = {
        'stream': stream,
        'stream_url': stream.get_stream_url(),
        'rtmp_url': stream.get_rtmp_url()
    }
    return render(request, 'main/nginxstream.html', context)

# ======================
# Функционал видеохостинга
# ======================

def upload_video(request):
    """
    Загрузка видеофайлов
    GET - показывает форму загрузки
    POST - сохраняет видео
    """
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            return redirect('video_list')
    else:
        form = VideoUploadForm()
    return render(request, 'video_hosting/upload_video.html', {'form': form})

def video_list(request):
    """
    Список всех видео с пагинацией
    """
    videos = Video.objects.all().order_by('-upload_date')
    paginator = Paginator(videos, 9)  # 9 видео на странице
    
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'video_hosting/video_list.html', {'videos': videos})

def video_detail(request, video_id):
    """
    Детальная страница видео
    """
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'video_hosting/video_detail.html', {'video': video})

# ======================
# Аутентификация и регистрация
# ======================

def register(request):
    """
    Регистрация новых пользователей
    Автоматически создает stream для нового пользователя
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Создаем стрим для нового пользователя
            Stream.objects.create(
                user=user,
                title=f'Stream {user.username}',
                stream_key=uuid.uuid4().hex[:12]
            )
            
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('stream_view')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})
