from django.contrib import admin
from .models import (
    Tag, Page, Gallery, GalleryImage, 
    ContentBlock, ServiceSlide, Client, Request
)
from adminsortable2.admin import SortableAdminBase, SortableAdminMixin, SortableInlineAdminMixin

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tag_type', 'show_in_menu', 'menu_title', 'menu_order')
    list_editable = ('show_in_menu', 'menu_title', 'menu_order')
    list_filter = ('tag_type', 'show_in_menu')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ContentBlockInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ContentBlock
    extra = 1
    fields = ('title', 'content', 'order', 'is_active')

@admin.register(Page)
class PageAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_home', 'show_slider', 'show_in_menu', 'menu_title', 'menu_order')
    list_editable = ('is_home', 'show_slider', 'show_in_menu', 'menu_title', 'menu_order')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    list_filter = ('is_home', 'show_in_menu')
    inlines = [ContentBlockInline]

class GalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'title', 'description', 'order')

@admin.register(Gallery)
class GalleryAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [GalleryImageInline]
    list_display = ('title', 'tag', 'page', 'created_at')
    list_filter = ('tag',)
    search_fields = ('title', 'description')
    autocomplete_fields = ['page']

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

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'service', 'created_at')
    list_filter = ('created_at', 'service')
    search_fields = ('name', 'phone')
    date_hierarchy = 'created_at'