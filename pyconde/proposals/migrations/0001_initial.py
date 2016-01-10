# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import pyconde.tagging


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '__first__'),
        ('taggit', '0002_auto_20150616_2121'),
        ('conference', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proposal',
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
                ('additional_speakers', models.ManyToManyField(related_name='proposal_participations', verbose_name='additional speakers', to='speakers.Speaker', blank=True)),
                ('audience_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience', to='conference.AudienceLevel')),
            ],
            options={
                'ordering': ['-pk'],
                'verbose_name': 'proposal',
                'verbose_name_plural': 'proposals',
                'permissions': (('see_proposal_author', 'Can always see the proposal author'),),
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(verbose_name='date')),
                ('slot', models.IntegerField(verbose_name='timeslot', choices=[(1, 'morning'), (2, 'afternoon')])),
                ('section', models.ForeignKey(verbose_name='section', to='conference.Section')),
            ],
            options={
                'ordering': ('date',),
                'verbose_name': 'timeslot',
                'verbose_name_plural': 'timeslots',
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='available_timeslots',
            field=models.ManyToManyField(to='proposals.TimeSlot', verbose_name='available timeslots', blank=True),
        ),
        migrations.AddField(
            model_name='proposal',
            name='conference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='duration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='duration', to='conference.SessionDuration'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='type', to='conference.SessionKind'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='speaker',
            field=models.ForeignKey(related_name='proposals', on_delete=django.db.models.deletion.PROTECT, verbose_name='speaker', to='speakers.Speaker'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='tags',
            field=pyconde.tagging.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='proposal',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='track', blank=True, to='conference.Track', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set([('date', 'slot', 'section')]),
        ),
    ]
