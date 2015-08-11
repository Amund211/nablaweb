# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from poll.models import Choice

from .utils import UserHasVotedMixin, create_poll

User = get_user_model()


class BaseVoteViewTest(TestCase):
    urls = "poll.urls"  # To test the url independently from root-url config

    def setUp(self):
        self.poll = create_poll(u"Er dette et spørsmål?", "Ja", "Nei", "Kanskje", "Vet ikke")
        self.vote_view = reverse("poll_vote", kwargs={"poll_id": self.poll.id})

        self.client = Client()

    def post_vote(self, choice_id=None):
        data = {"choice": choice_id} if choice_id is not None else {}
        self.client.post(self.vote_view, data)


class TestLoggedInVote(UserHasVotedMixin, BaseVoteViewTest):

    def setUp(self):
        super(TestLoggedInVote, self).setUp()

        self.username = "testuser"
        self.password = "mypass"
        self.user = User.objects.create_user(self.username, "asfd@asdf.no", self.password)
        self.client.login(username=self.username, password=self.password)

    def test_vote(self):
        choice = self.poll.choice_set.first()
        self.post_vote(choice.id)

        choice = Choice.objects.get(id=choice.id)
        self.assertUserHasVoted(self.user, self.poll)
        self.assertEqual(choice.votes, 1)

    def test_vote_without_choice(self):
        self.client.post(self.vote_view)
        self.post_vote()
        self.assertUserHasNotVoted(self.user, self.poll)

    def test_try_to_vote_again(self):
        choice = self.poll.choice_set.first()
        choice.vote(self.user)

        # Vote again through the vote view
        self.post_vote(2)


class NotLoggedIn(BaseVoteViewTest):
    def test_vote_unauthenticated(self):
        self.post_vote(1)
