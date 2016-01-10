# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pyconde.schedule.models
import django.utils.timezone
import sortedm2m.fields
import django.db.models.deletion
import pyconde.tagging


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '__first__'),
        ('cms', '0013_urlconfrevision'),
        ('conference', '__first__'),
        ('lightningtalks', '__first__'),
        ('taggit', '0002_auto_20150616_2121'),
        ('proposals', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteSchedulePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=100, verbose_name='title', blank=True)),
                ('row_duration', models.IntegerField(default=15, verbose_name='Duration of one row', choices=[(15, '15 Minutes'), (30, '30 Minutes'), (45, '45 Minutes'), (60, '60 Minutes')])),
                ('merge_sections', models.BooleanField(default=False, verbose_name='Merge different section into same table')),
                ('sections', models.ManyToManyField(to='conference.Section', verbose_name='sections', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(max_length=400, verbose_name='description')),
                ('abstract', models.TextField(verbose_name='abstract')),
                ('notes', models.TextField(verbose_name='notes', blank=True)),
                ('submission_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='submission date', editable=False)),
                ('modified_date', models.DateTimeField(null=True, verbose_name='modification date', blank=True)),
                ('language', models.CharField(default=b'de', max_length=5, verbose_name='language', choices=[(b'de', 'German'), (b'en', 'English')])),
                ('accept_recording', models.BooleanField(default=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start time', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end time', blank=True)),
                ('is_global', models.BooleanField(default=False, verbose_name='is global')),
                ('released', models.BooleanField(default=False, verbose_name='released')),
                ('slides_url', models.URLField(null=True, verbose_name='Slides URL', blank=True)),
                ('video_url', models.URLField(null=True, verbose_name='Video URL', blank=True)),
                ('max_attendees', models.PositiveSmallIntegerField(null=True, verbose_name='Max attendees', blank=True)),
                ('additional_speakers', models.ManyToManyField(related_name='session_participations', verbose_name='additional speakers', to='speakers.Speaker', blank=True)),
                ('audience_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience', to='conference.AudienceLevel')),
                ('available_timeslots', models.ManyToManyField(to='proposals.TimeSlot', verbose_name='available timeslots', blank=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference')),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='duration', to='conference.SessionDuration')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='type', to='conference.SessionKind')),
                ('location', models.ManyToManyField(to='conference.Location', verbose_name='location', blank=True)),
                ('proposal', models.ForeignKey(related_name='session', verbose_name='proposal', blank=True, to='proposals.Proposal', null=True)),
                ('section', models.ForeignKey(related_name='sessions', verbose_name='section', blank=True, to='conference.Section', null=True)),
                ('speaker', models.ForeignKey(related_name='sessions', on_delete=django.db.models.deletion.PROTECT, verbose_name='speaker', to='speakers.Speaker')),
                ('tags', pyconde.tagging.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='track', blank=True, to='conference.Track', null=True)),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
            },
            bases=(pyconde.schedule.models.LocationMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SideEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('start', models.DateTimeField(verbose_name='start time')),
                ('end', models.DateTimeField(verbose_name='end time')),
                ('is_global', models.BooleanField(default=False, verbose_name='is global')),
                ('is_pause', models.BooleanField(default=False, verbose_name='is break')),
                ('is_recordable', models.BooleanField(default=False, verbose_name='is recordable')),
                ('icon', models.CharField(blank=True, max_length=50, null=True, verbose_name='icon', choices=[(b'coffee', 'Coffee cup'), (b'glass', 'Glass'), (b'lightbulb-o', 'Lightbulb'), (b'moon-o', 'Moon'), (b'cutlery', 'Cutlery')])),
                ('video_url', models.URLField(null=True, verbose_name='Video URL', blank=True)),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference')),
                ('lightning_talks', sortedm2m.fields.SortedManyToManyField(help_text=None, to='lightningtalks.LightningTalk', blank=True)),
                ('location', models.ManyToManyField(to='conference.Location', verbose_name='location', blank=True)),
                ('section', models.ForeignKey(related_name='side_events', verbose_name='section', blank=True, to='conference.Section', null=True)),
            ],
            bases=(pyconde.schedule.models.LocationMixin, models.Model),
        ),
    ]
