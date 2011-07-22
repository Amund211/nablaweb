# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.events.models import Event
from nablaweb.events.forms import EventForm, EventFormPreview
from nablaweb.events.views import EventDetailView, EventListView, UserEventView

urlpatterns = patterns('nablaweb.events.views',

    # Administrasjon
    (r'^opprett/$', EventFormPreview(form=EventForm)),
    (r'^(?P<pk>\d{1,8})/endre$', EventFormPreview(form=EventForm)),
    (r'^(?P<event_id>\d{1,8})/admin$', 'administer'),
    (r'^(?P<event_id>\d{1,8})/slett$', 'delete'),

    # Offentlig
    (r'^$', EventListView.as_view()),
    url(r'^(?P<pk>\d{1,8})/$',
        EventDetailView.as_view(),
        name='event_detail',),

    # Bruker
    (r'^mine$', UserEventView.as_view()),
    (r'^(?P<event_id>\d{1,8})/registrering$', 'register_user'),

    # Eksporter
    (r'^(?P<event_id>\d{1,8})/eksporter$', 'ical_event'),
)
