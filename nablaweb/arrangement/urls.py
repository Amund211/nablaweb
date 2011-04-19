# arrangement/urls.py

from django.conf.urls.defaults import *

urlpatterns = patterns('arrangement.views',
# Administrasjon
    (r'^opprett/$', 'create'),
    (r'^(?P<event_id>\d+)/status$', 'status'),
    (r'^(?P<event_id>\d+)/endre$', 'edit'),
    (r'^(?P<event_id>\d+)/slett$', 'delete'),
# Offentlig
    (r'^$', 'list_events'),
    (r'^(?P<event_id>\d+)/$', 'show_event'),
# Bruker
    (r'^mine$', 'show_user'),
    (r'^(?P<event_id>\d+)/registrering$', 'registration'),
# Eksporter
    (r'^(?P<event_id>\d+)/eksporter$', 'ical_event'),
)
