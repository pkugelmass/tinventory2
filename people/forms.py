from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['ministry', 'role', 'profile_picture']