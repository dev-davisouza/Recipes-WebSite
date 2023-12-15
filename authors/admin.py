from django.contrib import admin
from authors.models import Authors


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin):
    list_display = ('username',)