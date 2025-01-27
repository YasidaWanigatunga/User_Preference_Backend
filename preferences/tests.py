from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class PreferencesTestCase(TestCase):

    def setUp(self):
        """Set up a test user before running tests."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='TestPass123',
            font_style='sans-serif'  # Ensure this matches the default
        )
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.preferences_url = reverse('preferences')

    def test_user_registration(self):
        """Test user registration functionality."""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPass123',
            'password2': 'TestPass123'
        }, follow=True)

        self.assertEqual(response.status_code, 200)  # Follow redirect to login page
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_fail(self):
        """Test registration failure due to password mismatch."""
        response = self.client.post(self.register_url, {
            'username': 'failuser',
            'email': 'failuser@example.com',
            'password': 'password1',
            'password2': 'password2'  # Different password
        }, follow=True)

        self.assertEqual(response.status_code, 200)  # Follow the redirect
        self.assertContains(response, 'Passwords do not match!')

    def test_user_login(self):
        """Test user login with valid credentials."""
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'TestPass123'
        }, follow=True)

        self.assertEqual(response.status_code, 200)  # Follow the redirect
        self.assertContains(response, "Preferences")  # Ensure preferences page loaded

    def test_user_login_fail(self):
        """Test login failure with incorrect password."""
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'WrongPass123'
        }, follow=True)

        self.assertEqual(response.status_code, 200)  # Follow the redirect
        self.assertContains(response, 'Invalid email or password')

    def test_preferences_view(self):
        """Test access to preferences page after login."""
        self.client.login(email='testuser@example.com', password='TestPass123')
        response = self.client.get(self.preferences_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preferences.html')

    def test_preferences_update(self):
        """Test updating preferences for logged-in user."""
        self.client.login(email='testuser@example.com', password='TestPass123')
        response = self.client.post(self.preferences_url, {
            'theme_color': 'dark',
            'font_style': 'serif',
            'layout_style': 'list',
            'email_notifications': True,
            'push_notifications': False,
            'notification_frequency': 'weekly',
            'profile_visibility': 'private',
            'data_sharing': False,
        }, follow=True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.theme_color, 'light')
        self.assertEqual(self.user.font_style, 'sans-serif')
        self.assertEqual(self.user.notification_frequency, 'daily')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test user logout."""
        self.client.login(email='testuser@example.com', password='TestPass123')
        response = self.client.get(reverse('logout'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You have been logged out.')
