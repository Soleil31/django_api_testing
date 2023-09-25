from django.contrib import admin
from .models import Product, Access, Lesson, LessonStatus


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ['name', 'owner']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_link', 'duration', 'created', 'updated']

@admin.register(LessonStatus)
class LessonStatus(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'watched_time', 'status']

@admin.register(Access)
class Access(admin.ModelAdmin):
    list_display = ['user', 'product']