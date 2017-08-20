from django.conf.urls import url, include
from . import views

urlpatterns = [
     
     url(r'^add(?P<type>[a-z]+)/$', views.AddResource, name='add-resource'),
     
     url(r'^link/(?P<slug>[-\w]+)$', views.ViewLink.as_view(), name='view-link'),
     
     url(r'^file/(?P<slug>[-\w]+)$', views.ViewFile.as_view(), name='view-file'),
     
     url(r'^editlink/(?P<slug>[-\w]+)$', views.EditLink.as_view(), name='edit-link'),
     
     url(r'^editfile/(?P<slug>[-\w]+)$', views.EditFile.as_view(), name='edit-file'),
     
     url(r'^deletelink/(?P<slug>[-\w]+)$', views.DeleteLink.as_view(), name='delete-link'),
     
     url(r'^deletefile/(?P<slug>[-\w]+)$', views.DeleteFile.as_view(), name='delete-file'),
     
     url(r'^$', views.ResourceList, name='resources'),
     
     ]