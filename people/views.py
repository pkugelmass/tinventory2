from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth.models import User
from datetime import datetime

def UserProfile(request, username):
    
    this_user = get_object_or_404(User, username=username)
    
    try:
        my_profile = Profile.objects.get(user=this_user)
    except:
        
        new_profile = Profile.objects.create(user=this_user)
        new_profile.last_login = datetime.now()
        new_profile.date_joined = datetime.now()
        new_profile.save()
    
    return render(request, 'people/profile.html', {'user':this_user})