from django.contrib import admin
from .models import Photo

# Register your models here.
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "created_at")
    search_fields = ("title", "description", "user__username")
    list_filter = ("created_at",)