from django import forms
from .models import Video

class VideoUploadForm(forms.ModelForm):
    """Форма для загрузки видео"""
    class Meta:
        model = Video  # Связанная модель
        fields = ['title', 'description', 'video_file']  # Поля формы
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Стилизация поля
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video_file': forms.FileInput(attrs={'class': 'form-control'}),
        }
