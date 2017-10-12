from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from tinventory.core.forms import SignUpForm, ProfileSignupSubform
from stronghold.decorators import public
from people.helpers import create_action
from people.models import Profile
from django.utils import timezone
from django.db import Error

@public
def signup(request):
    if request.method == 'POST':
        
        form = SignUpForm(request.POST)
        subform = ProfileSignupSubform(request.POST,request.FILES)
        
        if form.is_valid() and subform.is_valid():
            
            # Save the new user
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            
            # Create and populate the profile
            new_profile = Profile.objects.create(user=user)
            new_profile.ministry = subform.cleaned_data['ministry']
            new_profile.role = subform.cleaned_data['role']
            new_profile.profile_picture = subform.cleaned_data['profile_picture']
            new_profile.last_login = timezone.now()
            new_profile.save()
                
            # Note success and log the user in.
            create_action(user,'joined the site')
            login(request, user)
            return redirect('index')
            
    else:
        
        form = SignUpForm()
        subform = ProfileSignupSubform()
        
    return render(request, 'registration/signup.html', {'form': form, 'subform':subform,})