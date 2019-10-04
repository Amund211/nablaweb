from django.conf.urls import url
from .views import UnivDetailView, ExchangeListView, InfoDetailView, ExchangeFrontpageView, ExchangeNewsView, ExchangeNewsDetailView


urlpatterns = [
    url(r'^$', ExchangeFrontpageView.as_view(), name="ex_frontpage"),
    url(r'^info/(?P<pk>\d+)/$', InfoDetailView.as_view(), name="info_detail"),
    url(r'^(?P<pk>\d+)/$', UnivDetailView.as_view(), name="ex_detail_list"),
    url(r'^exchange-list$', ExchangeListView.as_view(), name="ex_list"),
    url(r'^exchange-news$', ExchangeNewsView.as_view(), name="ex_news"),
    url(r'^exchange-news/detail/(?P<pk>\d+)/(?P<slug>[-\w]*)$', ExchangeNewsDetailView.as_view(), name="ex_news_detail"),
]
