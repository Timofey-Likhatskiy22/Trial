from django.contrib import admin
from .models import ServiceSlide
from adminsortable2.admin import SortableAdminMixin

@admin.register(ServiceSlide)
class ServiceSlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'link', 'is_active')
        }),
    )