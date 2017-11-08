from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from transformations.models import Transformation, Ministry

class TestIndex(TestCase):
    
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200), 'Page should display when logged in.'
        self.assertContains(response, '<h2>Transformations'), 'Page should include Transformations heading.'
        self.assertContains(response, reverse('transformation-add')), 'Page should include link to create a new transformation.'
        
    def test_index_view_not_logged_in_bounces(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertNotEqual(response.status_code, 200), 'Should bounce away from page if not logged in.'
        
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
        
        
    def test_index_view_category_filter(self):
            
            obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
            obj.category='strategy'
            category_name = dict(Transformation.CATEGORIES)['strategy']
            obj.save()
                
            response = self.client.get(
                reverse('index'),
                data={
                    'ministry':'',
                    'category':'strategy',
                    'tags':'',
                    'status':'',
                }
            )
                
            self.assertContains(response, obj.title)
            self.assertContains(response, obj.get_absolute_url())
            self.assertContains(response, category_name)
        
    def test_index_view_category_filter_exclude(self):
        
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        obj.category='strategy'
        category_name = dict(Transformation.CATEGORIES)['strategy']
        obj.save()
            
        response = self.client.get(
            reverse('index'),
            data={
                'ministry':'',
                'category':'people',
                'tags':'',
                'status':'',
            }
        )
            
        self.assertNotContains(response, obj.title), 'Object\'s title should not appear.'
        self.assertNotContains(response, obj.get_absolute_url()), 'Object\'s link should not appear.'
        
    def test_all_filters_clear(self):
        
        t_list = [Transformation.objects.get_or_create(title='Test Transformation '+str(x))[0] for x in range(3)]
        
        response = self.client.get(
            reverse('index'),
            data={
                'ministry':'',
                'category':'',
                'tags':'',
                'status':'',
            }
        )
        
        for obj in t_list:
            self.assertContains(response, obj.title), 'Should display the title of each item.'
            self.assertContains(response, obj.get_absolute_url()), 'Should include a link to each item.'
        
    # I haven't written tests for TAG or STATUS because I think those things may still change.
    # Could also write tests that test multiple filters at once but that seems too complex for now.
    
class Test_Transformation_Detail_View(TestCase):
    
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
    
    def test_transformation_detail_view(self):
        
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        response = self.client.get(reverse('transformation-detail', kwargs={'slug':obj.slug}))
        self.assertEqual(response.status_code, 200), 'Page should display when logged in.'
        self.assertContains(response, obj.title[:10]), 'Page should show the object\'s title.'
        
    def test_transformation_detail_view_not_logged_in_bounces(self):
        
        obj = Transformation.objects.get_or_create(title='Test Transformation')[0]
        self.client.logout()
        response = self.client.get(reverse('transformation-detail', kwargs={'slug':obj.slug}))
        self.assertNotEqual(response.status_code, 200), 'Should bounce away from page if not logged in.'
        
class Test_Transformation_Add_View(TestCase):
    
    def setUp(self):
        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        
    def test_transformation_add_view(self):
        
        response = self.client.get(reverse('transformation-add'))
        self.assertEqual(response.status_code, 200), 'Page should display when logged in.'
        self.assertContains(response, '<h2>Add Transformation'), 'Page should show the title.'
        
    def test_transformation_add_view_not_logged_in_bounces(self):
        
        self.client.logout()
        response = self.client.get(reverse('transformation-add'))
        self.assertNotEqual(response.status_code, 200), 'Should bounce away from page if not logged in.'
        
    def test_transformation_add_view_accepts_valid_post_data(self):
        pass
    
    def test_transformation_add_view_rejects_invalid_post_data(self):
        pass
        # WHAT IS INVALID DATA?