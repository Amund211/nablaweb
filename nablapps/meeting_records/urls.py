"""
Urls for meeting_records app
"""
from django.conf.urls import url

from .views import MeetingRecordDetailView, MeetingRecordListView

urlpatterns = [
    url(r"^$", MeetingRecordListView.as_view(), name="meeting_record_list"),
    url(
        r"^(?P<pk>\d{1,8})/(?P<slug>[-\w]*)$",
        MeetingRecordDetailView.as_view(),
        name="meetingrecord_detail",
    ),
]
