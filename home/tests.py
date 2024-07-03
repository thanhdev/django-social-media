from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class HomePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_home_page_unauthenticated(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, 'Login to Your Account')
        self.assertNotContains(response, 'Welcome, testuser!')

    def test_home_page_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/authenticated_home.html')
        self.assertContains(response, 'Welcome, testuser!')
        self.assertContains(response, 'Logo')
        self.assertContains(response, 'Search...')

    def test_logout_link(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Sign out')

    def test_unauthenticated_user_doesnt_see_header(self):
        response = self.client.get(self.home_url)
        self.assertNotContains(response, 'Logo')
        self.assertNotContains(response, 'Search...')

    def test_authenticated_user_sees_profile_dropdown(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.home_url)
        self.assertContains(response, 'Profile')
        self.assertContains(response, 'Settings')
