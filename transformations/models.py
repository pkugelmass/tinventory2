from django.db import models
from django.core.urlresolvers import reverse
from .managers import ChoicesManager
#from resources.models import Attachment, Link
from autoslug import AutoSlugField
from people.models import Action
from django.contrib.contenttypes.models import ContentType
import os

# TAG MODELS

class Transformation_Tag(models.Model):
     name = models.CharField(max_length=20)
     
     class Meta:
          ordering = ['name']
          
     def __str__(self):
          return self.name

# TRANSFORMATION MODELS

class Transformation(models.Model):
     title = models.CharField("Transformation Title", max_length=100)
     ministry = models.ManyToManyField('Ministry')
     description = models.TextField("High-Level Description")
     problem = models.TextField("What problem is it trying to solve?", blank=True)
     specific_orgs = models.CharField("Which specific areas or other organizations are involved?", max_length=240, blank=True)
     primary_contact = models.CharField("Primary Contact", max_length=100, blank=True)
     
     CATEGORIES = (
          ('structure', 'Structure/Process'),
          ('strategy', 'Strategy/Policy'),
          ('service', 'Service Delivery'),
          ('people', 'People Development'),
          ('all', 'All of the Above'),
     )
     
     STATUSES = (
          ('direction', 'Defining Direction'),
          ('design', 'Design Stage'),
          ('implementation', 'Implementation'),
          ('sustainment', 'Sustainment'),
          ('complete', 'Past Transformation')
     )
     
     category = models.CharField(max_length=20, choices=CATEGORIES, blank=True)
     status = models.CharField(max_length=20, choices=STATUSES, blank=True)
     tags = models.ManyToManyField('Transformation_Tag', blank=True)
     archived = models.BooleanField(default=False)
     slug = AutoSlugField(populate_from='title')
     date_modified = models.DateTimeField(auto_now=True)
     
     class Meta:
          ordering = ['-date_modified']
     
     def get_absolute_url(self):
          return reverse('transformation-detail', kwargs={'slug':self.slug})
          
     def __str__(self):
          return self.title
          
     def ministries_list(self):
          return ', '.join(map(str, self.ministry.all()))
          
     def type(self):
          return 'transformation'
          
     def actions(self):
          return Action.objects.filter(target_id=self.pk, target_type=ContentType.objects.get_for_model(Transformation))
          
     def created(self):
          return Action.objects.filter(target_id=self.pk, target_type=ContentType.objects.get_for_model(Transformation), verb="created").first()
          
     def modified(self):
          return Action.objects.filter(target_id=self.pk, target_type=ContentType.objects.get_for_model(Transformation), verb="updated").first()

class Ministry(models.Model):
     abbrev = models.CharField(max_length=6)
     name = models.CharField(max_length=100)
     
     class Meta:
          ordering = ['abbrev']
     
     def __str__(self):
          return self.abbrev 
          
     def long(self):
          return self.abbrev + ' - ' + self.name
          
     objects = ChoicesManager()
     
