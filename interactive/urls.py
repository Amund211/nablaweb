from django.conf.urls import patterns, url
from .views import AdventCalendarView, AdventDoorView, QuizListView, QuizView, QuizResultView
from .views.quiz import quiz_reply, QuizScoreboardView, QuizResultDeleteView

urlpatterns = \
    patterns('',
             url(r'^julekalender/(?P<year>\d+)/(?P<number>\d+)/$',
                 AdventDoorView.as_view(),
                 name="advent_door"),
             url(r'^julekalender/(?P<year>\d+)/$',
                 AdventCalendarView.as_view(),
                 name="advent_calendar"),

             url(r'^quiz/$',
                 QuizListView.as_view(),
                 name="quiz_list"),
             url(r'^quiz/(?P<pk>[0-9]+)$',
                 QuizView.as_view(),
                 name="quiz"),
             url(r'^quiz/(?P<pk>[0-9]+)/reply$',
                 quiz_reply,
                 name="quiz_reply"),
             url(r'^quiz/(?P<pk>[0-9]+)/reply/delete$',
                 QuizResultDeleteView.as_view(),
                 name="quiz_result_delete"),
             url(r'^quiz/resultat/(?P<pk>[0-9]+)$',
                 QuizResultView.as_view(),
                 name="quiz_result"),
             url(r'^quiz/highscore/(?P<pk>[0-9]+)$',
                 QuizScoreboardView.as_view(),
                 name="quiz_score"),

             )
