from django.shortcuts import render
from .models import ServiceSlide

def home(request):
    slides = ServiceSlide.objects.filter(is_active=True).order_by('order')
    return render(request, 'services/index.html', {'slides': slides})