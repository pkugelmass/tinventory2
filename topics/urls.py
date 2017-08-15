from django.conf.urls import url, include
from . import views

urlpatterns = [
     
     # url(r'addlink/(?P<tID>\d+)$', views.AddLink.as_view(), name='add-link'), 
     
     # url(r'addfile/(?P<tID>\d+)$', views.AddFile.as_view(), name='add-file'),
     
     # url(r'viewlink/(?P<pk>\d+)$', views.ViewLink.as_view(), name='view-link'),
     
     # url(r'viewfile/(?P<pk>\d+)$', views.ViewFile.as_view(), name='view-file'),
     
     # url(r'editlink/(?P<pk>\d+)$', views.EditLink.as_view(), name='edit-link'),
     
     # url(r'editfile/(?P<pk>\d+)$', views.EditFile.as_view(), name='edit-file'),
     
     # url(r'deletelink/(?P<pk>\d+)$', views.DeleteLink.as_view(), name='delete-link'),
     
     # url(r'deletefile/(?P<pk>\d+)$', views.DeleteFile.as_view(), name='delete-file'),
     
     url(r'^$', views.TopicsList.as_view(), name='topics'),
     
     url(r'view/(?P<slug>[\w-]+)/$', views.TopicDetail.as_view(), name='topic-detail'),

     ]