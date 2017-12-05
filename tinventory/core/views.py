from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from tinventory.core.forms import SignUpForm, ProfileSignupSubform, FeedbackForm
from stronghold.decorators import public
from people.helpers import create_action
from people.models import Profile, Action
from transformations.models import Transformation
from sitepages.models import MiniFeedPage
from resources.models import Resource
from topics.models import Topic
from django.utils import timezone
from django.db import Error
from django.views.generic import TemplateView, FormView, DetailView
from django.core.mail import EmailMessage
from django.template.loader import get_template
from termsandconditions.decorators import terms_required
from termsandconditions.views import AcceptTermsView
from termsandconditions.models import TermsAndConditions
from django.utils.decorators import method_decorator

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

class HomePage(TemplateView):
    
    template_name = 'core/homepage.html'
    
    def get_context_data(self, **kwargs):
        my_context = {
            'transformation_count':Transformation.objects.count(),
            'resources_count':Resource.objects.count(),
            'topics_count':Topic.objects.exclude(level=0).count(),
            'users_count':Profile.objects.count(),
            'recent_actions':Action.objects.all()[:5],
            'site_updates_page':MiniFeedPage.objects.get(slug='site-updates')
        }
        
        context = super(TemplateView,self).get_context_data(**kwargs)
        context.update(my_context)
        
        return context
        
    @method_decorator(terms_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HomePage, self).dispatch(request, *args, **kwargs)
        
class MyAcceptTerms(AcceptTermsView):
    template_name = 'registration/accept_terms.html'
    
class MyViewTerms(DetailView):
    template_name = 'registration/view_terms.html'
    context_object_name = 'terms'
    
    def get_object(self,**kwargs):
        obj = TermsAndConditions.objects.latest('date_active').get_active()
        return obj
        
    
    
class FeedbackForm(FormView):
    
    form_class = FeedbackForm
    template_name = 'core/feedback_form.html'

    def form_valid(self,form):
        
        template = get_template('core/feedback_template.html')
        context = {
            'feedback_category': self.request.POST.get('feedback_category', ''),
            'content': self.request.POST.get('content', ''),
            'user': self.request.user,
            'path': self.request.META.get('HTTP_REFERRER'),
        }
        
        content = template.render(context)

        email = EmailMessage(
            "[Feedback] "+ self.request.POST.get('subject'),
            content,
            "T-Repo" +'',
            ['paul.kugelmass@ontario.ca'],
        )
        
        email.send()
        
        # It would be good to include a success message here.
        
        return redirect('home')
        
class SearchResults(TemplateView):
    template_name='core/search.html'