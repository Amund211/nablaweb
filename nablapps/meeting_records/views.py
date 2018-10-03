"""
Views for meeting records
"""
from django.views.generic import ListView, DetailView
from .models import MeetingRecord


class MeetingRecordDetailView(DetailView):
    """
    View showing a single meeting record along with a list of other meeting records.
    """
    model = MeetingRecord
    context_object_name = 'meeting_record'
    template_name = "meeting_records/meeting_record_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meeting_record_list'] = MeetingRecord.objects.order_by('-pub_date')
        return context


class MeetingRecordListView(ListView):
    """
    View listing all meeting records
    """
    model = MeetingRecord
    context_object_name = 'meeting_record_list'
    template_name = "meeting_records/meeting_record_list.html"
