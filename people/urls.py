from django.conf.urls import url, include
from . import views

urlpatterns = [
    
    url(r'^edit/(?P<username>[\w.@+-]+)/$', views.EditProfile, name="edit-profile"),
    
    url(r'^(?P<username>[\w.@+-]+)/$', views.UserProfile, name="user-profile"),
    
    
    
    
    
    ]