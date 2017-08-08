from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
     
     # TRANSFORMATION VIEWS
     
     url(r'^$', views.IndexView, name='index'),
     
     url(r'view/(?P<pk>\d+)$', views.TransformationDetail.as_view(), name='transformation-detail'),
     
     url(r'add/$', login_required(views.AddTransformation.as_view()), name='transformation-add'),
     
     url(r'edit/(?P<pk>\d+)$', login_required(views.EditTransformation.as_view()), name='transformation-edit'),
     
     url(r'delete/(?P<pk>\d+)$', login_required(views.DeleteTransformation.as_view()), name='transformation-delete'),
     
     # TRANSFORMATION-RESOURCE VIEWS
     
     url(r'addlink/(?P<tID>\d+)$', login_required(views.AddLink.as_view()), name='add-link'), 
     
     url(r'addfile/(?P<tID>\d+)$', login_required(views.AddFile.as_view()), name='add-file'),
     
     url(r'viewlink/(?P<pk>\d+)$', views.ViewLink.as_view(), name='view-link'),
     
     url(r'viewfile/(?P<pk>\d+)$', views.ViewFile.as_view(), name='view-file'),
     
     url(r'editlink/(?P<pk>\d+)$', login_required(views.EditLink.as_view()), name='edit-link'),
     
     url(r'editfile/(?P<pk>\d+)$', login_required(views.EditFile.as_view()), name='edit-file'),
     
     url(r'deletelink/(?P<pk>\d+)$', login_required(views.DeleteLink.as_view()), name='delete-link'),
     
     url(r'deletefile/(?P<pk>\d+)$', login_required(views.DeleteFile.as_view()), name='delete-file'),
     
     ]
     