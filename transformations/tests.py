from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Transformation

class TestIndex(TestCase):
    
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
    def test_index_view_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertNotEqual(response.status_code, 200)
        
    def test_index_view_showing_transformation(self):
        Transformation.objects.get_or_create(title='Test Transformation')
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Test Transformation')
        
    def test_index_view_links_to_transformation(self):
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        response = self.client.get(reverse('index'))
        self.assertContains(response, obj.get_absolute_url())