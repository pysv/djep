from django import forms
from django.contrib import admin

from ..speakers import models as speaker_models

from . import models


class ProposalAdminForm(forms.ModelForm):

    def clean_location(self):
        if not self.cleaned_data['location']:
            raise forms.ValidationError(ugettext('The location is mandatory.'))
        return self.cleaned_data['location']


class ProposalAdmin(admin.ModelAdmin):
    list_display = ("title", "kind", "conference", "duration", "speaker", "track")
    list_filter = ("conference", "kind", "duration", "track")
    form = ProposalAdminForm

    def add_view(self, *args, **kwargs):
        self.view = 'form'
        return super(ProposalAdmin, self).add_view(*args, **kwargs)

    def changelist_view(self, *args, **kwargs):
        self.view = 'list'
        return super(ProposalAdmin, self).changelist_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.view = 'form'
        return super(ProposalAdmin, self).change_view(*args, **kwargs)


class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'slot', 'section')


admin.site.register(models.Proposal, ProposalAdmin)
admin.site.register(models.TimeSlot, TimeSlotAdmin)
