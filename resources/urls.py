from django.conf.urls import url, include
from . import views

urlpatterns = [
     
     url(r'add(?P<type>[a-z]+)/$', views.AddResource, name='add-resource'),
     
     url(r'link/(?P<pk>\d+)$', views.ViewLink.as_view(), name='view-link'),
     
     url(r'file/(?P<pk>\d+)$', views.ViewFile.as_view(), name='view-file'),
     
     url(r'editlink/(?P<pk>\d+)$', views.EditLink.as_view(), name='edit-link'),
     
     url(r'editfile/(?P<pk>\d+)$', views.EditFile.as_view(), name='edit-file'),
     
     url(r'deletelink/(?P<pk>\d+)$', views.DeleteLink.as_view(), name='delete-link'),
     
     url(r'deletefile/(?P<pk>\d+)$', views.DeleteFile.as_view(), name='delete-file'),
     
     url(r'resources/$', views.ResourceList, name='resources'),
     
     ]