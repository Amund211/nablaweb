# -*- coding: utf-8 -*-

# arrangement/models.py

from django.db import models
from django.contrib.auth.models import User
from innhold.models import SiteContent
import datetime

class Event(SiteContent):
    class Meta:
        verbose_name_plural = "arrangement"

    organizer = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=False)

    event_start = models.DateTimeField(null=True, blank=False)
    event_end = models.DateTimeField(null=True, blank=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    deregistration_deadline = models.DateTimeField(null=True, blank=True)

    places = models.PositiveIntegerField(null=True, blank=True)

    def __unicode__(self):
        return u'%s, %s' % (self.headline, self.event_start.strftime('%d/%m/%y'))

    def free_places(self):
        return self.places - self.eventregistration_set.count()

    def is_full(self):
        return self.free_places() <= 0

    def is_attending(self, user):
        pass

    def registration_required(self):
        if self.registration_deadline is not None:
            return True
        return False

    def register_user(self, user):
        if datetime.datetime.now() > self.registration_deadline:
            return u"Påmeldingen har stengt."
        registration = self.eventregistration_set.filter(person=user)
        if registration:
            registration = registration[0]
        else:
            registration = EventRegistration(
                event=self,
                person=user,
                place=self.eventregistration_set.count()+1,
                )
            registration.save()
        if registration.place <= self.places:
            return u"Du er påmeldt."
        else:
            return u"Du står på venteliste."
        

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, blank=False, null=True)
    person = models.ForeignKey(User, blank=False, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    place = models.PositiveIntegerField(blank=False, null=True)


class NoShowDot(models.Model):
    event = models.ForeignKey(Event)
    person = models.ForeignKey(User)

    def __unicode__(self):
        return u'NoShowDot: %s, %s' % (self.event, self.person)
