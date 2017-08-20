from django import forms
from .models import File, Link, Resource
from transformations.models import Transformation, Ministry
from topics.models import Topic
from transformations.forms import ChoiceFieldEmpty
from mptt.forms import TreeNodeChoiceField

class FileForm(forms.ModelForm):
     class Meta:
          model = File
          fields = ['file','title','description', 'category', 'transformation', 'topics']
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40})}
          
     def __init__(self, *args, **kwargs):
          super(FileForm, self).__init__(*args, **kwargs)
          self.fields['topics'].widget.attrs['size']='15'
          
class LinkForm(forms.ModelForm):
     class Meta:
          model = Link
          fields = ['link','title','description', 'category', 'transformation', 'topics']
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}
          
     def __init__(self, *args, **kwargs):
          super(LinkForm, self).__init__(*args, **kwargs)
          
          self.fields['topics'].widget.attrs['size']='15'
          self.fields['link'].initial="http://"
          
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
          Topic.objects.all(), 
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

