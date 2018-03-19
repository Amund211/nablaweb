from django.http import Http404
from django.views.generic import TemplateView, DetailView, ListView
from hitcount.views import HitCountDetailView
from content.views import AdminLinksMixin, PublishedMixin, update_published_state
from utils.view_mixins import FlatPageMixin

from .models import Podcast, Season, get_season_count


class SeasonView(FlatPageMixin, TemplateView):
    template_name = "podcast/season.html"
    flatpages = [("info", "/skraattcast/")]

    def get_context_data(self, **kwargs):
        data = super(SeasonView, self).get_context_data(**kwargs)

        try:
            if 'number' in kwargs:
                number = kwargs['number']
                season = Season.objects.get(number=number)
            else:
                season = Season.objects.order_by('-number')[0]

            data['season'] = season
            data['season_name'] = season.name()

            update_published_state(Podcast)
            published = Podcast.objects.filter(season=season, published=True).order_by('-pub_date')
            data['podcast_list'] = published.filter(is_clip=False)
            data['podcast_clips'] = published.filter(is_clip=True)

            data['next'] = season.get_next()
            data['season_count'] = get_season_count()
            data['previous'] = season.get_previous()
        except Exception:
            raise Http404

        return data


class RssView(ListView):
    template_name = 'podcast/podcast.rss'
    content_type = 'application/xml'
    model = Podcast
    queryset = Podcast.objects.exclude(file='').filter(published=True, is_clip=False).order_by('-pub_date')


class PodcastDetailView(PublishedMixin, AdminLinksMixin, HitCountDetailView, DetailView):
    template_name = 'podcast/podcast_detail.html'
    model = Podcast
    context_object_name = "podcast"
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PodcastDetailView, self).get_context_data(**kwargs)
        context['season'] = season = self.object.season
        context['season_name'] = season.name()
        published = Podcast.objects.filter(season=season, published=True).order_by('-pub_date')
        context['podcast_clips'] = published.filter(is_clip=True)
        return context
