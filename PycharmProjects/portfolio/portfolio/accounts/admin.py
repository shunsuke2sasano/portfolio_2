from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'created_at', 'updated_at', 'deleted_at')  # 新しいフィールドを追加


# Register your models here.
