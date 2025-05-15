from django.test import TestCase
from django.urls import reverse

class HealthCheckTest(TestCase):
    def test_home_redirects_for_anonymous(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

