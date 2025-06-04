from django.contrib import admin
from .models import Category, Post, Reply

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_date')
    search_fields = ('name', 'description')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_date', 'views')
    list_filter = ('category', 'created_date', 'is_pinned')
    search_fields = ('title', 'content', 'author__username')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('content', 'author__username')