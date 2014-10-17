# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from podcast import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='podcast_list'),
        url(r'^(?P<podcast_id>\d+)/$', views.detail, name='podcast_detail'),
)
