# -*- coding: utf-8 -*-


from nablaweb.content.views import SiteContentListView, SiteContentDetailView
from nablaweb.news.models import News


class NewsListView(SiteContentListView):
    model = News


class NewsDetailView(SiteContentDetailView):
    model = News
