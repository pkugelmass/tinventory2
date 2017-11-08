from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponseRedirect
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tinventory.core import views as core_views
from people import views as people_views
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', lambda r: HttpResponseRedirect('transformations/')),
    
    url(r'^transformations/', include('transformations.urls')),
    
    url(r'^resources/', include('resources.urls')),
    
    url(r'^topics/', include('topics.urls')),
    
    url(r'^users/', include('people.urls')),
    
    url(r'^login/$', auth_views.login, name='login'),
    
    url(r'^logout/$', auth_views.logout, name='logout'),
    
    url(r'^signup/$', core_views.signup, name='signup'),
    
    url(r'^feed/$', people_views.ActivityFeed.as_view(), name='activity-feed'),
    
    url(r'^leaderboard/$', people_views.Leaderboard, name='leaderboard'),
    
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^site/', include(wagtail_urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns