from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Action
from django.contrib.auth.models import User
from datetime import datetime
from .forms import UserForm, ProfileForm
from django.urls import reverse
from django.contrib import messages
from .helpers import create_action
from django.views import generic
from django.conf import settings
from django.db.models import Sum, Count
from resources.models import Resource, Review
from django.contrib.auth import get_user_model
from transformations.models import Transformation, Ministry

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
        profile_form = ProfileForm(request.POST, request.FILES, instance=this_user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Your profile has been updated.')
            create_action(request.user, 'updated', Profile.objects.get(user=this_user))
            return redirect(reverse('user-profile', kwargs={'username':username}))
            
    else:
        
        user_form = UserForm(instance=this_user)
        profile_form = ProfileForm(instance=this_user.profile)
        context = {
            'user':this_user,
            'user_form':user_form,
            'profile_form':profile_form,
            }
    
    return render(request,'people/edit_profile.html', context)
    
class ActivityFeed(generic.ListView):
    model=Action
    template_name='people/activity_feed.html'
    
class Standings(object):
    
    def __init__(self,title,xaxis,measure,queryset):
        self.title=title
        self.xaxis=xaxis
        self.measure=measure
        self.queryset = queryset

def Leaderboard(request):
    
    User = get_user_model()
    
    leaderboards = [
        
        Standings(
            title='Most Active Users',
            xaxis='User',
            measure='Actions',
            queryset=User.objects.annotate(number=Count('actions')).filter(number__gt=0).order_by('-number')[:5]
            ),
                        
        Standings(
            title='Users with most Stars',
            xaxis='User',
            measure='Stars',
            queryset=User.objects.annotate(number=Sum('resources_created__reviews__rating')).filter(number__gt=0).order_by('-number')[:5]
            ),
        
        Standings(
            title='Top Resources',
            xaxis='Resource',
            measure='Stars',
            queryset=Resource.objects.annotate(number=Sum('reviews__rating')).filter(number__gt=0).order_by('-number')[:5]
            ),
            
                    
        Standings(
            title='Top Reviewers',
            xaxis='User',
            measure='Reviews',
            queryset=User.objects.annotate(number=Count('reviews')).filter(number__gt=0).order_by('-number')[:5]
            ),
            
        Standings(
            title='Transformations with Most Resources',
            xaxis='Transformation',
            measure='Resources',
            queryset=Transformation.objects.annotate(number=Count('resources')).filter(number__gt=0).order_by('-number')[:5]
            ),
            
        Standings(
            title='Ministry with most Transformations',
            xaxis='Ministry',
            measure='Transformations',
            queryset=Ministry.objects.annotate(number=Count('transformations')).filter(number__gt=0).order_by('-number')[:5]
            ),
            
        Standings(
            title='Ministry with most Users',
            xaxis='Ministry',
            measure='Users',
            queryset=Ministry.objects.annotate(number=Count('profiles')).filter(number__gt=0).order_by('-number')[:5]
            ),


        
    ]
    
    context = {'leaderboards':leaderboards}
    
    return render(request,'people/leaderboard.html',context)
    