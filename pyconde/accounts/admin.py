from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _

from . import models


class WithChildrenFilter(SimpleListFilter):
    title = _('Attending with children')
    parameter_name = 'children'

    def lookups(self, request, model_admin):
        return (('y', _('with children')),
                ('n', _('without children')))

    def queryset(self, request, queryset):
        if self.value() == 'y':
            queryset = queryset.filter(num_accompanying_children__gt=0)
        elif self.value() == 'n':
            queryset = queryset.filter(num_accompanying_children=0)
        return queryset


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_superuser',
        'is_reviewer', 'is_active', 'twitter', 'date_joined', 'organisation',
        'accept_pysv_conferences', 'accept_ep_conferences')
    list_filter = (WithChildrenFilter, 'accept_pysv_conferences',
                   'accept_ep_conferences')
    search_fields = ('email', 'twitter', 'organisation')

    def is_reviewer(self, instance):
        from pyconde.reviews import utils
        return utils.can_review_proposal(instance)
    is_reviewer.boolean = True
    is_reviewer.short_description = _('Can review')

admin.site.register(models.User, UserAdmin)


class BadgeStatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(models.BadgeStatus, BadgeStatusAdmin)
