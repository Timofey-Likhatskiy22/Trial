from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Tag(models.Model):
    TAG_TYPE_CHOICES = (
        ('global', 'Глобальный'),
        ('basic', 'Базовый'),
    )
    name = models.CharField("Название тега", max_length=100, unique=True)
    slug = models.SlugField("URL-тег", max_length=100, unique=True, blank=True)
    tag_type = models.CharField("Тип тега", max_length=10, choices=TAG_TYPE_CHOICES, default='basic')
    show_in_menu = models.BooleanField("Показывать в меню", default=False)
    menu_title = models.CharField("Название в меню", max_length=50, blank=True, null=True)
    menu_order = models.PositiveIntegerField("Порядок в меню", default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['menu_order']
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Page(models.Model):
    title = models.CharField("Заголовок страницы", max_length=200)
    slug = models.SlugField("URL", max_length=200, unique=True)
    content = models.TextField("Основной контент", blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)
    is_home = models.BooleanField("Главная страница", default=False)
    show_slider = models.BooleanField("Показывать слайдер", default=False)
    show_in_menu = models.BooleanField("Показывать в меню", default=False)
    menu_title = models.CharField("Название в меню", max_length=50, blank=True, null=True)
    menu_order = models.PositiveIntegerField("Порядок в меню", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    is_service = models.BooleanField("Является услугой", default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['menu_order']
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

class Gallery(models.Model):
    title = models.CharField("Название галереи", max_length=100)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, 
                           verbose_name="Базовый тег", limit_choices_to={'tag_type': 'basic'})
    description = models.TextField("Описание", blank=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    page = models.OneToOneField(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереи"

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField("Изображение", upload_to='gallery/')
    title = models.CharField("Название", max_length=100, blank=True)
    description = models.TextField("Описание", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Изображение галереи"
        verbose_name_plural = "Изображения галереи"

class ContentBlock(models.Model):
    page = models.ForeignKey(Page, related_name='blocks', on_delete=models.CASCADE)
    title = models.CharField("Заголовок блока", max_length=200, blank=True)
    content = models.TextField("Содержимое блока")  # Стандартное поле!
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Блок контента"
        verbose_name_plural = "Блоки контента"

class ServiceSlide(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to='slides/')
    link = models.URLField("Ссылка", max_length=500, default='#', blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активно", default=True)

    class Meta:
        verbose_name = "Слайд услуги"
        verbose_name_plural = "Слайды услуг"
        ordering = ['order']

    def __str__(self):
        return self.title

class Client(models.Model):
    name = models.CharField("Название компании", max_length=100)
    logo = models.ImageField("Логотип", upload_to='clients/')
    url = models.URLField("Сайт клиента", blank=True)

    def __str__(self):
        return self.name

class Request(models.Model):
    name = models.CharField("Имя", max_length=50)
    phone = models.CharField("Телефон", max_length=20)
    service = models.ForeignKey(
        Page,  # Изменено с Service на Page после рефакторинга
        on_delete=models.CASCADE, 
        verbose_name="Услуга",
        limit_choices_to={'is_service': True}  # Ограничиваем выбор только страницами-услугами
    )
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.name}"