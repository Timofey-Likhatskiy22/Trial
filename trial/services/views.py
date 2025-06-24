from django.shortcuts import render
from .models import ServiceSlide

def home(request):
    # Получаем активные слайды, отсортированные по порядку
    slides = ServiceSlide.objects.filter(is_active=True).order_by('order')
    
    # Проверяем, есть ли хотя бы один активный слайд
    has_slides = slides.exists()
    
    # Передаем данные в шаблон
    return render(request, 'services/index.html', {
        'slides': slides,
        'has_slides': has_slides
    })