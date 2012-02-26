# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from events.models import Event


class BedPres(Event):
    bpcid = models.CharField(verbose_name="BPC-id", max_length=16, unique=True, blank=True)

    class Meta:
        verbose_name = "bedriftspresentasjon"
        verbose_name_plural = "bedriftspresentasjoner"

    def register_user(self, user):
        super(Event, self).register_user(user)

    def deregister_user(self, user):
        super(Event, self).deregister_user(user)

    def move_user_to_place(self, user, place):
        super(Event, self).move_user_to_place(user)
