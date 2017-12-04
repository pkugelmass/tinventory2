from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from people.models import Profile

# much of this authentication stuff taken from https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        for x in self.fields:
            self.fields[x].required = True
            self.fields[x].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        (first, second,) = email.split("@")
        (domain, exn,) = second.split(".")
        if domain != "ontario" or exn != 'ca':
            raise forms.ValidationError("Domain must be 'ontario.ca'")
        return email 
        
class ProfileSignupSubform(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['ministry','role','profile_picture']
        
    def __init__(self,*args,**kwargs):
        super(ProfileSignupSubform,self).__init__(*args,**kwargs)
        for x in self.fields:
            self.fields[x].required = True
            self.fields[x].help_text = None
        self.fields['profile_picture'].required = False
        self.fields['profile_picture'].help_text="(Optional)"
        


class FeedbackForm(forms.Form):
    
    FEEDBACK_CATEGORIES = (
        ('bug','Reporting a Bug'),
        ('idea','Suggeting a Feature or Improvement'),
        ('complaint','Report a Pain Point'),
        ('question','Just wondering...'),
        ('compliments','We also take compliments.'),
        ('other','Other'),
    )
    
    feedback_category = forms.ChoiceField(choices=FEEDBACK_CATEGORIES)
    subject = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)