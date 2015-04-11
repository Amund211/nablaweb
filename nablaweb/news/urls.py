# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from news.views import NewsDetailView, NewsListView

urlpatterns = patterns('news.views',
    url(r'^$',
        NewsListView.as_view(),
        name='news_list'),
    url(r'^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$',
        NewsDetailView.as_view(),
        name='news_detail'),
)
