from django.shortcuts import render, get_object_or_404
from .models import Page, Tag, ServiceSlide

def home(request):
    home_page = Page.objects.filter(is_home=True).first()
    if not home_page:
        home_page = Page.objects.filter(show_in_menu=True).first()
    return render_page(request, home_page)

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render_page(request, page)

def render_page(request, page):
    if not page:
        return render(request, 'services/base.html', {'page': None})
    
    # Всегда инициализируем переменные слайдера
    slides = []
    has_slides = False
    
    # Получаем слайды только для главной страницы
    if page and page.is_home and page.show_slider:
        slides = ServiceSlide.objects.filter(is_active=True).order_by('order')
        has_slides = bool(slides)  # Преобразуем в булево значение

    context = {
        'page': page,
        'content_blocks': page.blocks.filter(is_active=True).order_by('order') if page else [],
        'slides': slides,
        'has_slides': has_slides,
    }
    
    # Если у страницы есть галерея
    if page and hasattr(page, 'gallery') and page.gallery:
        context['gallery'] = page.gallery
    
    return render(request, 'services/page.html', context)

def tag_page(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    pages = Page.objects.filter(tags=tag, show_in_menu=True).order_by('menu_order')
    return render(request, 'services/tag_page.html', {'tag': tag, 'pages': pages})