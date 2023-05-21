"""Users admin."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follow, User


@admin.register(User)
class UserAdmin(UserAdmin):
    """Users admin."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'first_name'
        )


@admin.register(Follow)
class SubscribeAdmin(admin.ModelAdmin):
    """Subscribe admin."""

    list_display = (
        'user',
        'author',
        )
