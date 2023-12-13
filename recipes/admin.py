from django.contrib import admin
from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'author')
    list_display_links = ('title',)
    search_fields = ('title', 'author', 'slug')
    list_filter = ('category', 'author', 'is_published')
    list_per_page = 9
    list_editable = "is_published",
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('title',)
        }


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
