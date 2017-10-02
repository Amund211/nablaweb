from django.contrib import admin
from .models import Poll, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 5
    fields = ('choice', 'votes', )
    fk_name = "poll"


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    fields = ['publication_date', 'question', 'is_current', 'users_voted', ]
    readonly_fields = ['users_voted', 'created_by']
    list_display = ('question', 'publication_date', 'is_current', 'created_by')
    list_filter = ['publication_date']
    inlines = [ChoiceInline]
