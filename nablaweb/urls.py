# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from nablaweb.news.feeds import RecentNews

from django.contrib import admin
admin.autodiscover()

from settings import GLOBAL_MEDIA_DIRS, MEDIA_ROOT, STATIC_URL

urlpatterns = patterns('',
    (r'^$', include('news.urls')),
    url(r'^login/$', 'accounts.views.login_user', name='auth_login'),
    url(r'^logout/$', 'accounts.views.logout_user', name='auth_logout'),
    url(r'^passord/reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^nyheter/', include('nablaweb.news.urls')),
    (r'^bedpres/', include('nablaweb.bedpres.urls')),
    (r'^arrangement/', include('nablaweb.events.urls')),
    (r'^brukere/', include('accounts.urls')),
    (r'^stillinger/', include('jobs.urls')),
    (r'^komite/', include('com.urls')),
#    (r'^gallery/', include('gallery.urls')),  # Kan ikke endres pga hardkoding i gallery-appen
    (r'^sitater/', include('quotes.urls')),
    (r'^nabladet/', include('nabladet.urls')),
    #(r'^referater/', include('meeting_records.urls')),
    (r'^kommentarer/', include('django.contrib.comments.urls')),
    (r'^poll/', include('poll.urls')),
    (r'^skraattcast/', include('skraattcast.urls')),

    # For å dele filer under utviklingen.
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': GLOBAL_MEDIA_DIRS[0]}),
    (r'^media/(?P<path>.*)$',  'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    # Redirecte til favicon
    (r'^favicon\.ico$', RedirectView.as_view(url=STATIC_URL + 'img/favicon.ico')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^feed/$', RecentNews()),
    (r'^search/', include('search.urls')),
)

urlpatterns += staticfiles_urlpatterns()
