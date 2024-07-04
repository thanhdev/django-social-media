from django.test import TestCase, Client
from django.urls import reverse
from .models import User
from django.core.exceptions import ValidationError


class HomePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse("home")
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_home_page_unauthenticated(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login") + "?next=/")

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/login.html")
        self.assertContains(response, "Login to Your Account")

    def test_home_page_authenticated(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertContains(response, "Welcome, testuser!")

    def test_logout_link(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign out")

    def test_unauthenticated_user_doesnt_see_header(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Logo")
        self.assertNotContains(response, "Search...")

    def test_authenticated_user_sees_profile_dropdown(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile")
        self.assertContains(response, "Settings")

    def test_create_post(self):
        self.assertFalse(self.user.posts.exists())
        self.client.login(username="testuser", password="12345")
        response = self.client.post(self.home_url, {"content": "This is a test post."})
        self.assertRedirects(response, self.home_url)
        post = self.user.posts.first()
        self.assertIsNotNone(post)
        self.assertEqual(post.content, "This is a test post.")


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")

    def test_registration_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/register.html")
        self.assertContains(response, "Create an Account")

    def test_successful_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complex_password123",
            "password2": "complex_password123",
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registration_with_existing_username(self):
        User.objects.create_user(username="existinguser", password="12345")
        data = {
            "username": "existinguser",
            "email": "newuser@example.com",
            "password1": "complex_password123",
            "password2": "complex_password123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "username", "A user with that username already exists."
        )

    def test_registration_with_mismatched_passwords(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "complex_password123",
            "password2": "different_password123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "password2", "The two password fields didn’t match."
        )

    def test_registration_with_weak_password(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "password",
            "password2": "password",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "password2", "This password is too common."
        )

    def test_registration_redirects_authenticated_user(self):
        User.objects.create_user(username="existinguser", password="12345")
        self.client.login(username="existinguser", password="12345")
        response = self.client.get(self.register_url)
        self.assertRedirects(response, reverse("home"))

    def test_registration_with_invalid_username(self):
        data = {
            "username": "invalid@username",
            "email": "newuser@example.com",
            "password1": "complex_password123",
            "password2": "complex_password123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "username",
            "Username can only contain letters, numbers, and underscores.",
        )

    def test_username_validator(self):
        from home.forms import validate_username

        # These should not raise an exception
        validate_username("validusername")
        validate_username("valid_username_123")

        # These should raise a ValidationError
        with self.assertRaises(ValidationError):
            validate_username("invalid@username")
        with self.assertRaises(ValidationError):
            validate_username("invalid username")
        with self.assertRaises(ValidationError):
            validate_username("invalid-username")


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.home_url = reverse("home")
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/login.html")

    def test_successful_login(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "12345"}
        )
        self.assertRedirects(response, self.home_url)

    def test_login_with_incorrect_password(self):
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive.",
        )

    def test_login_with_non_existent_user(self):
        response = self.client.post(
            self.login_url, {"username": "nonexistentuser", "password": "password"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive.",
        )

    def test_authenticated_user_redirected_from_login(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)
