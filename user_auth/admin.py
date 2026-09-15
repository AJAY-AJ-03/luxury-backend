from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'phone_number', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Contact', {'fields': ('phone_number',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'phone_number',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
