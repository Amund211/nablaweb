from django.contrib import admin
from .models import Application, ApplicationRound, Committee


@admin.register(ApplicationRound)
class ApplicationRoundAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    pass

@admin.register(Application)
class Application(admin.ModelAdmin):
    pass
