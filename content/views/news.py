# -*- coding: utf-8 -*-

from django.views.generic import DetailView, ListView

from content.templatetags import listutil
from content.models.news import News


class NewsListView(ListView):
    model = News
    context_object_name = 'news_list'
    template_name = 'news/news_list.html'
    paginate_by = 7  # Oddetall ser finest ut
    queryset = News.objects.select_related('content_type').exclude(priority=0).order_by('-pk')

    def get_context_data(self, **kwargs):
        """
        Deler innholdet opp i en featured_news og rader med to nyheter hver,
        news_rows = [[n1, n2], [n3, n4]] etc.
        """
        context = super(NewsListView, self).get_context_data(**kwargs)

        from django.contrib.flatpages.models import FlatPage
        try:
            context['sidebarinfo'] = FlatPage.objects.get(url="/forsideinfo/")
        except FlatPage.DoesNotExist:
            pass

        news_list = context['news_list']

        if news_list:
            context['featured_news'] = news_list[0]

            # Deler f.eks. opp [1, 2, 3, 4, 5] til [[1, 2], [3, 4], [5]]
            context['news_rows'] = listutil.row_split(news_list[1:], 2)

        return context


class NewsDetailView(DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'news/news_detail.html'
