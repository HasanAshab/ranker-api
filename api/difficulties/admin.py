from django.contrib import admin
from .models import Difficulty
from .forms import DifficultyForm


@admin.register(Difficulty)
class AuthorAdmin(admin.ModelAdmin):
    form = DifficultyForm
