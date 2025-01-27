"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from preferences import views

urlpatterns = [
    path('', views.user_login, name='home'),  # Redirect root URL to login page
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('preferences/', views.preferences, name='preferences'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('notification-settings/', views.notification_settings, name='notification_settings'),
    path('theme-settings/', views.theme_settings, name='theme_settings'),
    path('privacy-settings/', views.privacy_settings, name='privacy_settings'),
    path('admin/', admin.site.urls),
]
