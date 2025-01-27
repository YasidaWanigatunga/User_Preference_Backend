from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password,make_password

User = get_user_model()


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not all([username, email, password, password2]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken! Please choose another.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return redirect('login')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('preferences')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='/login/')
def preferences(request):
    """Main preferences view to display all settings"""
    user = request.user
    preferences_data = {
        'email_notifications': user.email_notifications,
        'push_notifications': user.push_notifications,
        'notification_frequency': user.notification_frequency,
        'theme_color': user.theme_color,
        'font_style': user.font_style,
        'layout_style': user.layout_style or 'list',
        'font_size': user.font_size,
        'profile_visibility': user.profile_visibility,
        'data_sharing': user.data_sharing
    }

    return render(request, 'preferences.html', {'preferences': preferences_data})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def account_settings(request):
    """Handles account settings including updating password securely"""
    user = request.user

    if request.method == 'POST':
        try:
            username = request.POST.get('username', user.username)
            email = request.POST.get('email', user.email)
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Check if password change is requested
            password_updated = False
            if old_password or new_password or confirm_password:
                if not old_password:
                    messages.error(request, "Please enter your current password to change it.")
                    return redirect('preferences')

                if not check_password(old_password, user.password):
                    messages.error(request, "Old password is incorrect.")
                    return redirect('preferences')

                if new_password != confirm_password:
                    messages.error(request, "New passwords do not match!")
                    return redirect('preferences')

                if old_password == new_password:
                    messages.error(request, "New password cannot be the same as the old password.")
                    return redirect('preferences')

                # Update the password securely
                user.password = make_password(new_password)
                password_updated = True
                messages.success(request, "Password updated successfully! Please log in again.")

            # Check for unique username and email
            if User.objects.exclude(id=user.id).filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose another.")
                return redirect('preferences')

            if User.objects.exclude(id=user.id).filter(email=email).exists():
                messages.error(request, "Email is already in use. Please use a different email.")
                return redirect('preferences')

            # Update username and email
            user.username = username
            user.email = email
            user.save()

            if not password_updated:
                messages.success(request, "Account settings updated successfully!")

            # Redirect appropriately
            if password_updated:
                logout(request)  # Log the user out after password change
                return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred while updating account settings: {str(e)}")

        return redirect('preferences')

    return render(request, 'preferences.html', {'preferences': user})



@login_required
def notification_settings(request):
    """Handles updating user notification settings"""
    user = request.user
    if request.method == 'POST':
        try:
            user.email_notifications = 'email_notifications' in request.POST
            user.push_notifications = 'push_notifications' in request.POST
            notification_frequency = request.POST.get('notification_frequency')

            if notification_frequency in ['daily', 'weekly', 'monthly', 'never']:
                user.notification_frequency = notification_frequency
            else:
                messages.error(request, "Invalid notification frequency selected.")
                return redirect('preferences')

            user.save()
            messages.success(request, "Notification settings updated successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred while updating notification settings: {str(e)}")

        return redirect('preferences')

    return render(request, 'preferences.html', {'preferences': user})


@login_required
def theme_settings(request):
    """Handles theme customization options"""
    user = request.user
    if request.method == 'POST':
        try:
            user.theme_color = request.POST.get('theme_color', user.theme_color)
            user.font_style = request.POST.get('font_style', user.font_style)
            user.layout_style = request.POST.get('layout_style', user.layout_style)
            user.font_size = request.POST.get('font_size', user.font_size)

            user.save()
            messages.success(request, "Theme settings updated successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred while updating theme settings: {str(e)}")

        return redirect('preferences')

    preferences = {
        'theme_color': user.theme_color,
        'font_style': user.font_style,
        'layout_style': user.layout_style,
        'font_size': user.font_size
    }

    return render(request, 'preferences.html', {'preferences': preferences})


@login_required
def privacy_settings(request):
    """Handles privacy settings like profile visibility and data sharing"""
    user = request.user
    if request.method == 'POST':
        try:
            profile_visibility = request.POST.get('profile_visibility')

            if profile_visibility not in ['public', 'private']:
                messages.error(request, "Invalid profile visibility choice.")
                return redirect('preferences')

            user.profile_visibility = profile_visibility
            user.data_sharing = 'data_sharing' in request.POST

            user.save()
            messages.success(request, "Privacy settings updated successfully!")

        except Exception as e:
            messages.error(request, f"An error occurred while updating privacy settings: {str(e)}")

        return redirect('preferences')

    preferences = {
        'profile_visibility': user.profile_visibility,
        'data_sharing': user.data_sharing
    }

    return render(request, 'preferences.html', {'preferences': preferences})
