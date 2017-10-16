from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Transformation, Ministry

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
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Test Transformation')
        self.assertContains(response, obj.get_absolute_url())
        
    def test_index_view_ministry_filter(self):
        
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        min = Ministry.objects.get_or_create(abbrev="MSW", name="Ministry of Silly Walks")[0]
        obj.ministry=[1]
        obj.save()
            
        response = self.client.get(
            reverse('index'),
            data={
                'ministry':'MSW',
                'category':'',
                'tags':'',
                'status':'',
            }
        )
            
        self.assertContains(response, obj.title)
        self.assertContains(response, obj.get_absolute_url())
        self.assertContains(response, min.abbrev)
        
    def test_index_view_ministry_filter_exclude(self):
        
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        min = Ministry.objects.create(abbrev="MSW", name="Ministry of Silly Walks")
        min2 = Ministry.objects.create(abbrev="MFG", name="Ministry of Funny Gaits")
        obj.ministry=[min2]
        obj.save()
            
        response = self.client.get(
            reverse('index'),
            data={
                'ministry':'MSW',
                'category':'',
                'tags':'',
                'status':'',
            }
        )
            
        self.assertNotContains(response, obj.title), 'Object\'s title should not appear.'
        self.assertNotContains(response, obj.get_absolute_url()), 'Object\'s link should not appear.'