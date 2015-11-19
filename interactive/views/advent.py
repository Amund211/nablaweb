from django.views.generic import DetailView, ListView
from interactive.models.advent import AdventCalendar, AdventDoor, AdventParticipation
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime


class AdventDoorView(DetailView):
    model = AdventDoor
    pk_url_kwarg = "number"
    context_object_name = "door"

    def get_template_names(self):
        return self.object.template

    def get_context_data(self, **kwargs):
        context = super(AdventDoorView, self).get_context_data(**kwargs)
        context['calendar'] = context['door'].calendar
        return context


class AdventCalendarView(ListView):
    model = AdventDoor
    context_object_name = "doors"

    def dispatch(self, request, *args, **kwargs):
        self.calendar = AdventCalendar.objects.get(year=kwargs['year'])
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return self.calendar.template

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(calendar=self.calendar)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calendar'] = self.calendar
        return context


@login_required
def participate_in_competition(request, year, number):

    calendar = AdventCalendar.objects.get(year=year)
    door = AdventDoor.objects.get(
        calendar=calendar,
        number=number
    )

    if door.is_lottery and door.is_today:
        user = request.user
        text = request.POST.get('text')
        AdventParticipation.objects.update_or_create(
            user=user,
            door=door,
            defaults={
                'text': text,
                'when': datetime.now()
            }
        )
    return redirect(door.get_absolute_url())
