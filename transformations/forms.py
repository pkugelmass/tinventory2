from django import forms
from .models import Ministry, Transformation, Transformation_Tag

# FORM HELPER STUFF ---------

# Custom field class to add an empty choice at the top of the drop-down box.
class ChoiceFieldEmpty(forms.ChoiceField):
     
     def __init__(self,*args,**kwargs):
          super(ChoiceFieldEmpty,self).__init__(*args,**kwargs)
          self.choices = [('',' ')] + self.choices
          
# TRANSFORMATION FORMS ------------

class TransformationFilterForm(forms.Form):
     
     ministry = forms.ModelChoiceField(
          Ministry.objects.all().order_by('abbrev'),
          label="Ministry",
          empty_label='', 
          required=False
          )
          
     category = ChoiceFieldEmpty(
          choices = Transformation.CATEGORIES, 
          label="Category", 
          required=False
          )
          
     tags = forms.ModelChoiceField(
          Transformation_Tag.objects.all().order_by('name'),
          label="Area of Focus",
          empty_label='',
          required=False,
          )
          
     status = ChoiceFieldEmpty(
          choices = Transformation.STATUSES, 
          label="Status", 
          required=False
          )
     
class TransformationForm(forms.ModelForm):
     
     class Meta:
          model = Transformation
          fields = ['title','ministry','specific_orgs','description','problem','category', 'tags',\
               'status','primary_contact',]
          widgets = {
               'description':forms.Textarea(attrs={'rows':4,'cols':40}),
               'problem':forms.Textarea(attrs={'rows':4,'cols':40}),}
          help_texts = {
               'ministry':'You can select more than one. Ctrl-click to select all that apply.',
               'tags':'What are some other areas of focus? You can select more than one. Ctrl-click to select all that apply.',
               'category':'What is the primary focus?',
               'problem':'What problem is it trying to solve?',
               'specific_orgs':'What specific internal/external orgs/groups are involved?',
               }

     def __init__(self, *args, **kwargs):
          super(TransformationForm, self).__init__(*args, **kwargs)
          self.fields['ministry'].widget.attrs['size']='7'
          self.fields['tags'].widget.attrs['size']='7'