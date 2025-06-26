from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tag/<slug:tag_slug>/', views.tag_page, name='tag_page'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]