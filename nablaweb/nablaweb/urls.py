# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from news.feeds import RecentNews
# nødvendig for django-wiki
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern

from filebrowser.sites import site


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^$', include('news.urls')),
    (r'^', include('content.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/login.html'}, name='auth_login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
    url(r'^passord/reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^nyheter/', include('news.urls')),
    (r'^bedpres/', include('bedpres.urls')),
    (r'^arrangement/', include('events.urls')),
    (r'^brukere/', include('accounts.urls')),
    (r'^stillinger/', include('jobs.urls')),
    (r'^komite/', include('com.urls')),
    (r'^sitater/', include('quotes.urls')),
    (r'^nabladet/', include('nabladet.urls')),
    (r'^referater/', include('meeting_records.urls')),
    (r'^kommentarer/', include('django_comments.urls')),
    (r'^poll/', include('poll.urls')),
    (r'^podcast/', include('podcast.urls')),

    # For å dele filer under utviklingen.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$',  'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # Redirecte til favicon
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.ico')),

    (r'^admin/', include(admin.site.urls)),

    url(r'^feed/$', RecentNews()),
    (r'^search/', include('search.urls')),
)

urlpatterns += staticfiles_urlpatterns()

# django-wiki
urlpatterns += patterns('',
    (r'^wiki/notifications/', get_nyt_pattern()),
    (r'^wiki/', get_wiki_pattern())
)
