from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Notification settings
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    NOTIFICATION_FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('never', 'Never')
    ]
    notification_frequency = models.CharField(
        max_length=10,
        choices=NOTIFICATION_FREQUENCY_CHOICES,
        default='daily'
    )

    # Theme settings
    THEME_COLOR_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark')
    ]
    FONT_STYLE_CHOICES = [
        ('sans-serif', 'Sans Serif'),
        ('serif', 'Serif'),
        ('monospace', 'Monospace')
    ]
    LAYOUT_STYLE_CHOICES = [
        ('grid', 'Grid'),
        ('list', 'List')
    ]
    FONT_SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large')
    ]

    theme_color = models.CharField(
        max_length=10,
        choices=THEME_COLOR_CHOICES,
        default='light'
    )
    font_style = models.CharField(
        max_length=15,
        choices=FONT_STYLE_CHOICES,
        default='sans-serif'
    )
    layout_style = models.CharField(
        max_length=10,
        choices=LAYOUT_STYLE_CHOICES,
        default='list'
    )
    font_size = models.CharField(
        max_length=10,
        choices=FONT_SIZE_CHOICES,
        default='medium'
    )

    # Privacy settings
    PROFILE_VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private')
    ]

    profile_visibility = models.CharField(
        max_length=10,
        choices=PROFILE_VISIBILITY_CHOICES,
        default='public'
    )
    data_sharing = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
