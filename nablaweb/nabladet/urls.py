# -*- coding: utf-8 -*-

from django.conf.urls import *
from nabladet.views import NabladListView, NabladDetailView

urlpatterns = patterns('nablad.views',
    # Offentlig
    url(r'^$', 
        NabladListView.as_view( context_object_name = "nablad_list" ),
        name='nablad_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$', 
        NabladDetailView.as_view( context_object_name = "nablad" ),
        name='nablad_detail'),
)
