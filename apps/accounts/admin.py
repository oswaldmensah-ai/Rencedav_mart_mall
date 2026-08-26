"""Register custom User with Django's admin site."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'full_name', 'is_admin', 'is_active', 'date_joined')
    list_filter   = ('is_admin', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering      = ('-date_joined',)

    fieldsets = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal',     {'fields': ('first_name', 'last_name', 'phone_number', 'address')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser',
                                     'groups', 'user_permissions')}),
        ('Dates',        {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':  ('email', 'first_name', 'last_name', 'password1', 'password2',
                        'is_admin', 'is_staff', 'is_active'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')
