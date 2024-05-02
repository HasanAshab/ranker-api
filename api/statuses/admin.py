from django.contrib import admin
from .models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
