from django.utils.functional import cached_property

from content.exceptions import (EventFullException,
                                RegistrationAlreadyExists,
                                RegistrationNotOpen)
from bpc_client import BPCEvent
from bpc_client.exceptions import BPCResponseException
from accounts.models import NablaUser as User
from .utils import get_bpc_user_dictionary


class RegistrationInfo(object):
    """A simple class used for the return value of register_user."""
    def __init__(self, attending):
        self.attending = attending
        self.waiting = not attending


class BPCEventMixin(object):
    """Mixin-class to add the same methods for registration as the Event-model from content."""
    bpcid = None

    @cached_property
    def bpc_event(self):
        return BPCEvent(bpc_id=self.bpcid)

    def register_user(self, user):
        try:
            user_dict = get_bpc_user_dictionary(user)
            is_attending = self.bpc_event.add_attending(**user_dict)
            return RegistrationInfo(is_attending)
        except BPCResponseException as e:
            if e.bpc_error_code == "402":
                raise EventFullException(event=self, user=user)
            elif e.bpc_error_code == "405":
                raise RegistrationAlreadyExists(event=self, user=user)
            elif e.bpc_error_code in ("408", "409"):
                raise RegistrationNotOpen(event=self, user=user)
            raise e

    def deregister_user(self, user):
        self.bpc_event.rem_attending(username=user.username)

    def get_attendance_list(self):
        return User.objects.filter(username__in=self.bpc_event.attending_usernames)

    def get_waiting_list(self):
        return User.objects.filter(username__in=self.bpc_event.waiting_usernames)

    def is_registered(self, user):
        return self.is_attending(user) or self.is_waiting(user)

    def is_attending(self, user):
        return user.username in self.bpc_event.attending_usernames

    def is_waiting(self, user):
        return user.username in self.bpc_event.waiting_usernames

    def free_places(self):
        return self.bpc_event.seats_available

    def is_full(self):
        return self.free_places() == 0

    def users_attending(self):
        return self.bpc_event.this_attending

    def users_waiting(self):
        return len(self.bpc_event.waiting_usernames)

    def percent_full(self):
        places = self.bpc_event.seats
        if places != 0:
            return ((places - self.free_places())*100) / places
        else:
            return 100

    def open_for_classes(self):
        min_year = self.bpc_event.min_year
        max_year = self.bpc_event.max_year
        if max_year == '99':
            max_year = ''
        if min_year == max_year:
            return min_year
        else:
            return min_year + '-' + max_year


class BedpresNoModel(BPCEventMixin):
    def __init__(self, bpcid):
        self.bpcid = bpcid
