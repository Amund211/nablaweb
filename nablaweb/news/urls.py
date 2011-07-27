# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *
from nablaweb.news.forms import NewsForm, NewsFormPreview
from nablaweb.news.views import NewsDetailView, NewsListView, NewsDeleteView

urlpatterns = patterns('nablaweb.news.views',

    # Administrasjon
    (r'^opprett/$', NewsFormPreview(form=NewsForm)),
    (r'^(?P<pk>\d{1,8})/endre/$', NewsFormPreview(form=NewsForm)),
    (r'^(?P<pk>\d{1,8})/slette/$', NewsDeleteView.as_view()),

    # Offentlig
    url(r'^$',
        NewsListView.as_view(),
        name='news_list'),
    url(r'^(?P<pk>\d{1,8})/$',
        NewsDetailView.as_view(),
        name='news_detail'),
)
