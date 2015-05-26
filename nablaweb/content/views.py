from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Album


class AlbumOverview(ListView):
    model = Album
    context_object_name = "albums"
    template_name = "content/album_overview.html"
    paginate_by = 10
    queryset = Album.objects.exclude(visibillity='h').order_by('created_date')

    def get_context_data(self, **kwargs):
        context = super(AlbumOverview, self).get_context_data(**kwargs)
        return context


class AlbumView(TemplateView):

    template_name = "content/album.html"
    visible = False

    def dispatch(self, request, *args, **kwargs):
        result = super(AlbumView, self).dispatch(request, *args, **kwargs)
        if self.visible:
            return result
        else:
            return redirect('auth_login')

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        num = int(kwargs['num'])
        pk = int(kwargs['pk'])
        album = Album.objects.filter(pk=pk)[0]
        context['album'] = album
        self.visible = album.is_visible()

        images = album.images.all()
        paginator = Paginator(images, 1)
        try:
            page_obj = paginator.page(num)
        except (EmptyPage, PageNotAnInteger):
            page_obj = paginator.page(1)

        context['page_obj'] = page_obj
        context['image'] = page_obj.object_list[0]

        return context
