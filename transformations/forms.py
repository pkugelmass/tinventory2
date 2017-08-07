from django import forms
from .models import Ministry, Transformation, Attachment, Link
#from taggit.models import Tag 

# FORM HELPER STUFF ---------

# Custom field class to add an empty choice at the top of the drop-down box.
class ChoiceFieldEmpty(forms.ChoiceField):
     
     def __init__(self,*args,**kwargs):
          super(ChoiceFieldEmpty,self).__init__(*args,**kwargs)
          self.choices = [('',' ')] + self.choices
          
# TRANSFORMATION FORMS ------------

class TransformationFilterForm(forms.Form):
     
     #TAG_LIST = ( ( tag, tag.name ) for tag in Tag.objects.all().order_by('name') )
     
     ministry__abbrev = ChoiceFieldEmpty(choices = Ministry.objects.choices_list(), label="Ministry", required=False)
     category = ChoiceFieldEmpty(choices = Transformation.CATEGORIES, label="Category", required=False)
     status = ChoiceFieldEmpty(choices = Transformation.STATUSES, label="Status", required=False)
     #tags__name = ChoiceFieldEmpty(choices = TAG_LIST, label="Tag", required=False)
     
class TransformationForm(forms.ModelForm):
     
     class Meta:
          model = Transformation
          fields = ['title','ministry','specific_orgs','description','problem','category', \
               'status','primary_contact'] #PULLED OUT TAGS
          widgets = {
               'description':forms.Textarea(attrs={'rows':4,'cols':40}),
               'problem':forms.Textarea(attrs={'rows':4,'cols':40}),
               #'ministry':forms.SelectMultiple(attrs={choices:Ministry.objects.choices_list()}),
               }
          #choices = {'ministry':Ministry.objects.choices_list()}
          help_texts = {
               'ministry':'Crtl-click to select all that apply.',
               #'tags':'Ctrl-click to select all that apply.'
               }
               
# RESOURCES FORMS ---------------

class AttachmentForm(forms.ModelForm):
     class Meta:
          model = Attachment
          fields = ['resource','title','description','transformation'] #PULLED OUT TAGS
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}
          
class LinkForm(forms.ModelForm):
     class Meta:
          model = Link
          fields = ['resource','title','description','transformation'] #PULLED OUT TAGS
          widgets = {'description':forms.Textarea(attrs={'rows':3,'cols':40}),}