from django.conf.urls import url, include
from . import views
from resources.views import AddResource

urlpatterns = [
     
     url(r'^$', views.TopicsList.as_view(), name='topics'),
     
     url(r'(?P<slug>[-\w]+)/add(?P<type>[a-z]+)/$', AddResource, {'base':'topic'}, name='resource-add-topic'),
     
     url(r'(?P<slug>[-\w]+)/$', views.TopicDetail, name='topic-detail'),
     
     #url(r'add(?P<type>[a-z]+)/$', AddResource, {'base':'topic'}, name='resource-add-topic-base'),

     ]