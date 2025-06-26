from django import template
from django.utils.safestring import mark_safe
from services.models import Tag, Page
import logging

logger = logging.getLogger(__name__)
register = template.Library()

@register.simple_tag
def generate_menu():
    try:
        menu_html = ''
        
        # Меню "Вывески"
        sign_tag = Tag.objects.filter(slug='vyveski', show_in_menu=True).first()
        if sign_tag:
            sign_pages = Page.objects.filter(tags=sign_tag, show_in_menu=True).order_by('menu_order')
            menu_html += f'''
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="/tag/{sign_tag.slug}/" id="navbarDropdownSigns" 
                   role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    {sign_tag.menu_title or sign_tag.name}
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdownSigns">
                    <li><a class="dropdown-item" href="/tag/{sign_tag.slug}/">Все {sign_tag.menu_title or sign_tag.name}</a></li>
                    <li><hr class="dropdown-divider"></li>
            '''
            
            for page in sign_pages:
                menu_title = page.menu_title or page.title
                menu_html += f'<li><a class="dropdown-item" href="{page.get_absolute_url()}">{menu_title}</a></li>'
            
            menu_html += '</ul></li>'
        
        # Меню "Наружная реклама"
        outdoor_tag = Tag.objects.filter(slug='naruzhnaya-reklama', show_in_menu=True).first()
        if outdoor_tag:
            outdoor_pages = Page.objects.filter(tags=outdoor_tag, show_in_menu=True).order_by('menu_order')
            menu_html += f'''
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="/tag/{outdoor_tag.slug}/" id="navbarDropdownOutdoor" 
                   role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    {outdoor_tag.menu_title or outdoor_tag.name}
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdownOutdoor">
                    <li><a class="dropdown-item" href="/tag/{outdoor_tag.slug}/">Все {outdoor_tag.menu_title or outdoor_tag.name}</a></li>
                    <li><hr class="dropdown-divider"></li>
            '''
            
            for page in outdoor_pages:
                menu_title = page.menu_title or page.title
                menu_html += f'<li><a class="dropdown-item" href="{page.get_absolute_url()}">{menu_title}</a></li>'
            
            menu_html += '</ul></li>'
        
        # Меню "Интерьерная реклама"
        interior_tag = Tag.objects.filter(slug='interernaya-reklama', show_in_menu=True).first()
        if interior_tag:
            interior_pages = Page.objects.filter(tags=interior_tag, show_in_menu=True).order_by('menu_order')
            menu_html += f'''
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="/tag/{interior_tag.slug}/" id="navbarDropdownInterior" 
                   role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    {interior_tag.menu_title or interior_tag.name}
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdownInterior">
                    <li><a class="dropdown-item" href="/tag/{interior_tag.slug}/">Все {interior_tag.menu_title or interior_tag.name}</a></li>
                    <li><hr class="dropdown-divider"></li>
            '''
            
            for page in interior_pages:
                menu_title = page.menu_title or page.title
                menu_html += f'<li><a class="dropdown-item" href="{page.get_absolute_url()}">{menu_title}</a></li>'
            
            menu_html += '</ul></li>'
        
        # Остальные пункты меню
        menu_items = [
            ('lazernaya-rezka', 'Лазерная резка'),
            ('suvenirnaya-produktsiya', 'Сувенирная продукция'),
            ('o-nas', 'О нас')
        ]
        
        for slug, title in menu_items:
            page = Page.objects.filter(slug=slug, show_in_menu=True).first()
            if page:
                menu_title = page.menu_title or page.title
                menu_html += f'''
                <li class="nav-item">
                    <a class="nav-link" href="{page.get_absolute_url()}">
                        {menu_title}
                    </a>
                </li>
                '''
        
        # Возвращаем HTML как безопасную строку
        return mark_safe(menu_html)
    
    except Exception as e:
        logger.exception("Ошибка при генерации меню")
        return mark_safe('<li class="nav-item"><span class="text-danger">Ошибка меню</span></li>')