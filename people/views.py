from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from django.contrib.auth.models import User
from datetime import datetime
from .forms import UserForm, ProfileForm
from django.urls import reverse
from django.contrib import messages

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
    
def EditProfile(request, username):
    
    this_user = get_object_or_404(User, username=username)
    
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=this_user)
        profile_form = ProfileForm(request.POST, instance=this_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Your profile has been saved.')
            return redirect(reverse('user-profile', kwargs={'username':username}))
            
    else:
        
        user_form = UserForm(instance=this_user)
        profile_form = ProfileForm(instance=this_user)
        context = {
            'user':this_user,
            'user_form':user_form,
            'profile_form':profile_form,
            }
    
    return render(request,'people/edit_profile.html', context)