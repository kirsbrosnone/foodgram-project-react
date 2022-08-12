from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Пользователь', {'fields': (
            'email', 'username', 'first_name', 'last_name',
        )}),
        ('Пароль', {'fields': (
            'password',
        )}),
        ('Права', {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'user_permissions',
        )}),
        ('Информация', {'fields': (
            'date_joined', 'last_login'
        )}),
    )

    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'is_staff',
    )
    list_filter = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
