# -*- coding: utf-8 -*-

# Admingrensesnitt for stillingsannonser-appen

from django.contrib import admin
from django.forms import ModelForm
from django.forms import MultipleChoiceField
from jobs.models import Advert, Company, RelevantForChoices, TagChoices

#class RelevantForAdminForm(ModelForm):
#    RELEVANT_FOR_CHOICES = ((u'B', u'Biofysikk'), (u'T', u'Teknisk fysikk'), (u'I', u'Industriell matematikk'))
#    relevant_for = MultipleChoiceField(choices=RELEVANT_FOR_CHOICES)
#    class Meta:
#        model = Advert

class AdvertAdmin(admin.ModelAdmin):
#    relevant_for_form = RelevantForAdminForm
    pass
    
class CompanyAdmin(admin.ModelAdmin):
    pass
        
class RelevantForChoicesAdmin(admin.ModelAdmin):
    pass
    
class TagChoicesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Advert, AdvertAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(RelevantForChoices, RelevantForChoicesAdmin)
admin.site.register(TagChoices, TagChoicesAdmin)
