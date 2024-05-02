from django.contrib import admin
from .models import Difficulty


@admin.register(Difficulty)
class DifficultyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
