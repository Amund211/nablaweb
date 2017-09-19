
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

from content.feeds.news import RecentNews
import django_nyt.urls


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^login/$',
        login,
        {'template_name': 'admin/login.html'}
        ),
    url(r'^logout/$', logout),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^album/', include('contentapps.album.urls')),
    url(r'^blogg/', include('contentapps.blog.urls')),
    url(r'', include('content.urls')),
    url(r'^feed/$', RecentNews()),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^notifications/', django_nyt.urls.get_pattern()),
]
