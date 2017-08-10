from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
     
     # TRANSFORMATION VIEWS
     
     url(r'^$', views.IndexView, name='index'),
     
     url(r'view/(?P<pk>\d+)$', views.TransformationDetail.as_view(), name='transformation-detail'),
     
     url(r'add/$', views.AddTransformation.as_view(), name='transformation-add'),
     
     url(r'edit/(?P<pk>\d+)$', views.EditTransformation.as_view(), name='transformation-edit'),
     
     url(r'delete/(?P<pk>\d+)$', views.DeleteTransformation.as_view(), name='transformation-delete'),
     
     # TRANSFORMATION-RESOURCE VIEWS
     
     url(r'addlink/(?P<tID>\d+)$', views.AddLink.as_view(), name='add-link'), 
     
     url(r'addfile/(?P<tID>\d+)$', views.AddFile.as_view(), name='add-file'),
     
     url(r'viewlink/(?P<pk>\d+)$', views.ViewLink.as_view(), name='view-link'),
     
     url(r'viewfile/(?P<pk>\d+)$', views.ViewFile.as_view(), name='view-file'),
     
     url(r'editlink/(?P<pk>\d+)$', views.EditLink.as_view(), name='edit-link'),
     
     url(r'editfile/(?P<pk>\d+)$', views.EditFile.as_view(), name='edit-file'),
     
     url(r'deletelink/(?P<pk>\d+)$', views.DeleteLink.as_view(), name='delete-link'),
     
     url(r'deletefile/(?P<pk>\d+)$', views.DeleteFile.as_view(), name='delete-file'),
     
     url(r'resources/$', views.ResourceList, name='resources'),
     
     ]
     