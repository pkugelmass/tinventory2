from django.conf.urls import url, include
from . import views
from resources.views import AddResource

urlpatterns = [
     
     url(r'^$', views.TopicsList.as_view(), name='topics'),
     
     url(r'view/(?P<slug>[\w-]+)/$', views.TopicDetail.as_view(), name='topic-detail'),
     
     url(r'(?P<topic_slug>[\w-]+)/add(?P<type>[a-z]+)/$', AddResource, name='resource-add-topic'),
     
     url(r'add(?P<type>[a-z]+)/$', AddResource, name='resource-add-topic-base'),

     ]