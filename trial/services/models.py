from django.db import models

class Service(models.Model):
    title = models.CharField("Название услуги", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='services/')
    slug = models.SlugField("URL-адрес", unique=True)

    def __str__(self):
        return self.title
    
class ServiceSlide(models.Model):
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to='slides/')
    link = models.CharField("Ссылка", max_length=100, default='#', help_text="Например: #outdoor")
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
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    created_at = models.DateTimeField("Дата заявки", auto_now_add=True)

    def __str__(self):
        return f"Заявка от {self.name}"