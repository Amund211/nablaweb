from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="forum-index"),
    path('<channel_id>/', ChannelView.as_view(), name="channel-index"),
    path('<channel_id>/<thread_id>/', ThreadView.as_view(), name="thread-view"),
]
