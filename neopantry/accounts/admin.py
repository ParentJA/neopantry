# Django imports.
from django.contrib import admin
from django.contrib.auth import get_user_model

__author__ = 'Jason Parent'

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'username', 'first_name', 'last_name', 'email', 'photo', 'date_of_birth', 'phone_number', 'is_staff',
        'is_active', 'date_joined',
    )
    list_display = (
        'username', 'first_name', 'last_name', 'email', 'photo', 'date_of_birth', 'phone_number', 'is_staff',
        'is_active', 'date_joined',
    )
