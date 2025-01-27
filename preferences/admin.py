from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined', 'theme_color', 'profile_visibility')
    list_filter = ('is_active', 'is_staff', 'theme_color', 'profile_visibility')
    search_fields = ('username', 'email')

    fieldsets = (
        ('Account Settings', {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Notification Settings', {'fields': ('email_notifications', 'push_notifications', 'notification_frequency')}),
        ('Theme Settings', {'fields': ('theme_color', 'font_style', 'layout_style', 'font_size')}),
        ('Privacy Settings', {'fields': ('profile_visibility', 'data_sharing')}),
    )

    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

admin.site.register(CustomUser, CustomUserAdmin)
