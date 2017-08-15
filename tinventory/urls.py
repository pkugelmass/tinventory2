from django.conf.urls import url, include
from django.contrib import admin
from django.http import HttpResponseRedirect
from . import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tinventory.core import views as core_views

urlpatterns = [
    
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', lambda r: HttpResponseRedirect('transformations/')),
    
    url(r'^transformations/', include('transformations.urls')),
    
    url(r'^resources/', include('resources.urls')),
    
    url(r'^topics/', include('topics.urls')),
    
    url(r'^login/$', auth_views.login, name='login'),
    
    url(r'^logout/$', auth_views.logout, name='logout'),
    
    url(r'^signup/$', core_views.signup, name='signup'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns