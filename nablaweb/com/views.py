# -*- coding: utf-8 -*-

# Views for com-appen

from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import DetailView
from com.models import *

class ShowPage(DetailView):
    model = ComPage
    slug_field = 'com'
   
    def get_context_data(self, **kwargs):
        context = super(ShowPage, self).get_context_data(**kwargs)
        c = self.get_object()
        context['members'] = ComMember.objects.filter(com = c)
