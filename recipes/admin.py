from django.contrib import admin
from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
