# -*- coding: utf-8 -*-


import datetime
from django.contrib import messages as django_messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, RequestContext, loader
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from nablaweb.news.views import NewsListView, NewsDetailView, NewsDeleteView
from nablaweb.events.models import Event, EventRegistration
from nablaweb.bedpres.models import BedPres
from itertools import chain
from events.event_calendar import EventCalendar

# Administrasjon

def _admin_mov(request, instance):
    user_list = request.POST.getlist('user')
    text = request.POST.get('text')
    try:
        place = int(text)
        for user in user_list:
            user = User.objects.get(username=user)
            if instance.is_registered(user):
                instance.move_user_to_place(user, place)
    except (ValueError, User.DoesNotExist): pass
_admin_mov.short = 'mov'
_admin_mov.info = 'Flytt til'


def _admin_add(request, instance):
    text = request.POST.get('text')
    try:
        user = User.objects.get(username=text)
        instance.register_user(user)
    except User.DoesNotExist: pass
_admin_add.short = 'add'
_admin_add.info = 'Legg til'


def _admin_del(request, instance):
    user_list = request.POST.getlist('user')
    for user in user_list:
        try:
            user = User.objects.get(username=user)
            instance.deregister_user(user)
        except User.DoesNotExist: pass
_admin_del.short = 'del'
_admin_del.info = 'Fjern'


def administer(request, pk,
               actions=(_admin_add, _admin_mov, _admin_del),
               view='event_admin'):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        action_name = request.POST.get('action')
        for action in actions:
            if action.short == action_name:
                action(request, event)
                break

        # Unngå at handlingen utføres på nytt dersom brukeren laster siden om igjen
        return HttpResponseRedirect(reverse(view, kwargs={'pk': pk}))

    registrations = event.eventregistration_set.all().order_by('number')
    return render_to_response('events/event_administer.html',
                              {'event': event,
                               'registrations': registrations,
                               'actions': [(a.short, a.info) for a in actions]},
                              context_instance=RequestContext(request))


class EventDeleteView(NewsDeleteView):
    model = Event


# Offentlig

def calendar(request, year=None, month=None):
    """Renders a calendar with events from the chosen month

    Args:
        request (HttpRequest) : Django request object
    """
    if not year:
        year = datetime.date.today().year
    if not month:
        month = datetime.date.today().month

    events = Event.objects.order_by('event_start').filter(
        event_start__year=year, event_start__month=month
    )
    cal = EventCalendar(events).formatmonth(year, month)
    return render(request, 'events/event_list.html', {'calendar': mark_safe(cal)})

class EventListView(ListView):
    model = Event
    context_object_name = "event_list"
    queryset = Event.objects.all() 

    # TODO: For performance reasons, only fetch the needed events.
    # That is, from Monday in the first week, to Sunday in the last week.

    def get_context_data(self, **kwargs):
        # Get the context from the superclass
        context = super(EventListView, self).get_context_data(**kwargs)
        
        # Penalties
        user = self.request.user
        if user.is_authenticated():
            context['penalty_list'] = user.eventpenalty_set.all()

        # Functions to be used
        from datetime import date, timedelta
        from calendar import monthrange

        today = date.today()

        # Set parameters from url. (/year/month)
        try:
            year = int(self.args[0])
        except IndexError:
            year = today.year

        try:
            month = int(self.args[1])
        except IndexError:
            month = today.month
        
        monthdays = monthrange(year, month)
        weeknodelta = date(year, month, monthdays[1]).isocalendar()[1] - date(year, month, 1).isocalendar()[1]
        
        # Weeks to be displayed
        if (weeknodelta == 5):
            weeks = 6
        else:
            weeks = 5

        # Get the monday at the start of the calendar
        first = date(year, month, 1)
        first_monday = first - timedelta(days=first.weekday())
        #  last_sunday = first + timedelta(weeks=weeks, days=6)

        # Object to add to context
        calendar = {'first': first, 'weeks': []}

        for week in range(0, weeks):
            # Add an empty week, with weeknumber
            calendar['weeks'].append({'days': []})
            for daynumber in range(0, 7):
                # Get the day
                day = first_monday + timedelta(days=week * 7 + daynumber)

                # If monday, get the weeknumber and add to current week
                if day.weekday() == 0:
                    calendar['weeks'][week]['weeknumber'] = day.isocalendar()[1]

                # Get the events and bedpresses which start at the current day,
                # or between two dates if an end date exists
                all_events = chain(context['event_list'], BedPres.objects.all())
                events = [event for event in all_events
                        if (event.event_end and event.event_start.date() <= day
                        and day <= event.event_end.date()) or event.event_start.date() == day]

                # Add it to the week
                calendar['weeks'][week]['days'].append({
                    'date': day.day,
                    'events': events,
                    'differentmonth': (day.month != month),
                    'current': (day == today),
                })

        # Add next and previous
        calendar['prev'] = first_monday - timedelta(days=1)
        calendar['next'] = first + timedelta(days=31)

        # Add it to the request context
        context['calendar'] = calendar
        return context


class EventDetailView(NewsDetailView):
    model = Event
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)
        object_name = self.object.content_type.model
        event = self.object
        user = self.request.user

        if user.is_anonymous():
            context['is_registered'] = False
        else:
            # Innlogget, så sjekk om de er påmeldt
            context['is_registered'] = event.is_registered(user)
            context['is_attending'] = event.is_attending(user)
            if context['is_registered']:
                # Henter eventregistration for denne brukeren hvis han/hun er påmeldt
                context['eventregistration'] = event.eventregistration_set.get(user=user)
        return context


# Bruker

class UserEventView(TemplateView):
    template_name = 'events/event_showuser.html'

    def get_context_data(self, **kwargs):
        context_data = super(UserEventView, self).get_context_data(**kwargs)
        user = self.request.user
        context_data['user'] = user
        if user.is_authenticated():
            context_data['eventregistration_list'] = user.eventregistration_set.all().order_by('event__event_start') 
            context_data['is_on_a_waiting_list'] = bool( filter(EventRegistration.is_waiting_place , context_data['eventregistration_list']) )
            context_data['penalty_list'] = user.eventpenalty_set.all()
        return context_data

@login_required
def register_user(request, event_id):
    messages = {
        'noreg'     : 'Ingen registrering.',
        'unopened'  : 'Påmeldingen har ikke åpnet.',
        'closed'    : 'Påmeldingen har stengt.',
        'full'      : 'Arrangementet er fullt.',
        'attend'    : 'Du er påmeldt.',
        'queue'     : 'Du står på venteliste.',
        'reg_exists': 'Du er allerede påmeldt.',
        'not_allowed' : 'Du har ikke lov til å melde deg på dette arrangementet.',
        }
    event = get_object_or_404(Event, pk=event_id)
    
    if event.registration_start and event.registration_start > datetime.datetime.now():
        token = 'unopened'
    elif event.registration_deadline and event.registration_deadline < datetime.datetime.now():
        token = 'closed'
    elif not event.allowed_to_attend(request.user):
        token = 'not_allowed'
    else:
        token = event.register_user(request.user)

    message = messages[token]
    django_messages.add_message(request, django_messages.INFO, message)
    return HttpResponseRedirect(event.get_absolute_url())

@login_required
def deregister_user(request, event_id):
    messages = {
        'not_reg': 'Du verken var eller er påmeldt.',
        'dereg_closed': 'Fristen for å melde seg av er gått ut.',
        'not_allowed': 'Ta kontakt med ArrKom for å melde deg av.',
        'dereg': 'Du er meldt av arrangementet.',
        }
    event = get_object_or_404(Event, pk=event_id)
    
    if event.deregistration_closed is None:
        token = 'not_allowed'
    elif  event.deregistration_closed():
        token = 'dereg_closed'
    else:
        token = event.deregister_user(request.user)

    message = messages[token]
    django_messages.add_message(request, django_messages.INFO, message)
    return HttpResponseRedirect(event.get_absolute_url())


# Eksporter

def ical_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    template = loader.get_template('events/event_icalendar.ics')
    context = Context({'event_list': (event,),})
    response = HttpResponse(template.render(context), mimetype='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=Nabla_%s.ics' % event.title.replace(' ', '_')
    return response


def ical_user(request):
    return HttpResponse("Not implemented.")
