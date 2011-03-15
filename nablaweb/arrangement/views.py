# arrangement/views.py

from nablaweb.arrangement.models import Event, NoShowDot
from nablaweb.arrangement.forms import EventForm
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib.auth.models import User
import datetime

# Administrasjon

def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            event = Event(title=cd['title'],
                          summary=cd['summary'],
                          body=cd['body'],
                          location=cd['location'],
                          event_start=cd['event_start'],
                          )
            event.save()
            return HttpResponseRedirect('/arrangement/%d/' % event.id)
    else:
        form = EventForm(
            initial={'event_start': datetime.datetime.now()},
            )
    return render_to_response('arrangement/create.html', RequestContext(request, {'form': form}))

def status(request, event_id):
    return HttpResponse("Not implemented.")

def edit(request, event_id):
    return HttpResponse("Not implemented.")

def delete(request, event_id):
    return HttpResponse("Not implemented.")


# Offentlig

def overview(request):
    return render_to_response('arrangement/overview.html', {'event_list': Event.objects.all()})

def details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render_to_response('arrangement/details.html', {'event': event})


# Bruker

def show_user(request):
    event_list = request.user.events_attending.all()
    dot_list = request.user.noshowdot_set.all()
    print event_list
    return render_to_response('arrangement/showuser.html', {'event_list': event_list, 'dot_list': dot_list, 'member': request.user})

def registration(request, event_id):
    return HttpResponse("Not implemented.")

def register(request, event_id):
    return HttpResponse("Not implemented.")


# Eksporter

def ical_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    template = loader.get_template('arrangement/icalendar.ics')
    context = Context({'event_list': (event,),})
    response = HttpResponse(template.render(context), mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.title.replace(' ', '_')
    return response

def ical_user(request):
    return HttpResponse("Not implemented.")
