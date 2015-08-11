# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from django.template.defaultfilters import slugify
from com.models import ComPage, ComMembership


class ShowPage(DetailView):
    template_name = 'com/com_details.html'
    model = ComPage
    context_object_name = 'com'

    def canonical_name(self):
        return slugify(self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ShowPage, self).get_context_data(**kwargs)
        com = self.get_object().com
        context['members'] = ComMembership.objects.filter(com=com)
        context['compages'] = ComPage.objects.all().order_by('com__name')
        return context
