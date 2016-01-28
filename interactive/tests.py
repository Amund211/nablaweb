from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from random import random
from datetime import datetime, timedelta


from .models import *
from .models.quiz import QuizReplyTimeout, QuestionReply

User = get_user_model()


class AdventTests(TestCase):
    def setUp(self):
        self.cal = AdventCalendar.objects.create(
            year=2015
        )
        self.doors = []
        for i in range(1, 24):
            door = AdventDoor.objects.create(
                template="interactive/advent_door_base.html",
                content="Test",
                number=i,
                calendar=self.cal
            )
            self.doors.append(door)

    def test_update(self):
        for d in self.doors:
            d.content = "Hello world"
            d.save()

        self.cal.year += 1
        self.cal.save()

    def test_delete(self):
        for d in self.doors:
            d.delete()

        self.cal.delete()


class BaseQuizTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(
            title="Test quiz",
            is_timed=True,
            duration=100
        )
        self.questions = []
        for i in range(1, 24):
            question = QuizQuestion.objects.create(
                question="Something?",
                correct_alternative=1,
                alternative_1="One",
                alternative_2="Two",
                alternative_3="Three",
                alternative_4="Four",
                quiz=self.quiz
            )
            self.questions.append(question)


class QuizTests(BaseQuizTest):

    def test_update(self):
        for q in self.questions:
            q.question = "Hello world?"
            q.save()

        self.quiz.save()

    def test_delete(self):
        for d in self.questions:
            d.delete()

        self.quiz.delete()

    def test_reply(self):
        data = {'{id}_alternative'.format(id=q.id): int(random() * 4 + 1) for q in self.questions}
        self.client.post(reverse('quiz_reply', kwargs={'pk': self.quiz.id}), data=data)


class QuizReplyTest(BaseQuizTest):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username="quizlover")
        self.reply = QuizReply.objects.create(
            user=self.user,
            scoreboard=self.quiz.scoreboard,
            start=datetime.now(),
            when=datetime.now()
        )

    def test_add_question_replies(self):
        replies = [(q, q.correct_alternative) for q in self.questions]
        self.reply.add_question_replies(replies)
        self.assertEqual(self.reply.get_correct_count(), self.reply.get_question_count())

    def test_add_question_replies_raises_exception_on_timeout(self):
        self.quiz.duration = 1
        self.quiz.save()
        self.reply.start = datetime.now() - timedelta(seconds=3600)
        with self.assertRaises(QuizReplyTimeout):
            self.reply.add_question_replies([])

    def test_only_possible_to_have_one_answer_per_question(self):
        replies = [(q, q.correct_alternative) for q in self.questions]
        self.reply.add_question_replies(replies)
        self.reply.add_question_replies(replies)
        self.assertEqual(len(replies), QuestionReply.objects.filter(quiz_reply=self.reply).count())
