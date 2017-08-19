from django import forms
from .models import Attachment, Link, Resource
from transformations.models import Transformation, Ministry
from topics.models import Topic
from transformations.forms import ChoiceFieldEmpty
from mptt.forms import TreeNodeChoiceField

class AttachmentForm(forms.ModelForm):
     class Meta:
          model = Attachment
          fields = ['resource','title','description', 'category', 'transformation', 'topics']
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}
          
class LinkForm(forms.ModelForm):
     class Meta:
          model = Link
          fields = ['resource','title','description','category', 'transformation', 'topics'] 
          widgets = {
               'description':forms.Textarea(attrs={'rows':3,'cols':40}),
          }
          
class ResourceFilterForm(forms.Form):
     
     RESOURCE_TYPES = ( ('File', 'File'), ('Link','Link') )
     
     resourcetype = ChoiceFieldEmpty(
          choices=RESOURCE_TYPES, 
          label = 'Type', 
          required=False)
     
     category = ChoiceFieldEmpty(
          choices=Resource.CATEGORIES, 
          label = 'Resource Category', 
          required=False)
     
     topic = TreeNodeChoiceField(
          Topic.objects.filter(level__gt=0), 
          label='Topic', 
          empty_label='', 
          required=False)
     
     transformation = forms.ModelChoiceField(
          Transformation.objects.all().order_by('title'),
          label='Transformation', 
          empty_label='', 
          required=False)
     
     ministry = ChoiceFieldEmpty(
          choices = Ministry.objects.choices_list(), 
          label="Ministry", 
          required=False)

