# -*- coding: utf-8 -*-

from poll.models import Poll

def poll_context(request):
    poll = Poll.objects.filter(is_current=True)
    try:
        return {'poll': poll[0]}
    except:
        return {}
