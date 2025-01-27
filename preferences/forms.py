from django import forms
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


class AccountSettingsForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email_notifications', 'push_notifications', 'notification_frequency']

    def clean_notification_frequency(self):
        frequency = self.cleaned_data.get('notification_frequency')
        if frequency not in ['daily', 'weekly', 'monthly', 'never']:
            raise forms.ValidationError("Invalid frequency option selected.")
        return frequency

class ThemeSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['theme_color', 'font_style', 'layout_style', 'font_size']

    def clean(self):
        cleaned_data = super().clean()
        theme_color = cleaned_data.get("theme_color")
        font_style = cleaned_data.get("font_style")
        layout_style = cleaned_data.get("layout_style")
        font_size = cleaned_data.get("font_size")

        if theme_color not in ['light', 'dark']:
            raise forms.ValidationError("Invalid theme color option selected.")
        if font_style not in ['sans-serif', 'serif', 'monospace']:
            raise forms.ValidationError("Invalid font style option selected.")
        if layout_style not in ['grid', 'list']:
            raise forms.ValidationError("Invalid layout style option selected.")
        if font_size not in ['small', 'medium', 'large']:
            raise forms.ValidationError("Invalid font size option selected.")

        return cleaned_data
