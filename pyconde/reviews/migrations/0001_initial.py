# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import pyconde.tagging


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '__first__'),
        ('taggit', '0002_auto_20150616_2121'),
        ('proposals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='content')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
                ('deleted', models.BooleanField(default=False, verbose_name='deleted')),
                ('deleted_date', models.DateTimeField(null=True, verbose_name='deleted at', blank=True)),
                ('deleted_reason', models.TextField(null=True, verbose_name='deletion reason', blank=True)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(related_name='deleted_comments', verbose_name='deleted by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
            },
        ),
        migrations.CreateModel(
            name='ProposalMetaData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_comments', models.PositiveIntegerField(default=0, verbose_name='number of comments')),
                ('num_reviews', models.PositiveIntegerField(default=0, verbose_name='number of reviews')),
                ('latest_activity_date', models.DateTimeField(null=True, verbose_name='latest activity', blank=True)),
                ('latest_comment_date', models.DateTimeField(null=True, verbose_name='latest comment', blank=True)),
                ('latest_review_date', models.DateTimeField(null=True, verbose_name='latest review', blank=True)),
                ('latest_version_date', models.DateTimeField(null=True, verbose_name='latest version', blank=True)),
                ('score', models.FloatField(default=0.0, verbose_name='score')),
            ],
            options={
                'verbose_name': 'proposal metadata',
                'verbose_name_plural': 'proposal metadata',
            },
        ),
        migrations.CreateModel(
            name='ProposalVersion',
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
                ('pub_date', models.DateTimeField(verbose_name='publication date')),
                ('additional_speakers', models.ManyToManyField(related_name='proposalversion_participations', verbose_name='additional speakers', to='speakers.Speaker', blank=True)),
                ('audience_level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='target-audience', to='conference.AudienceLevel')),
                ('available_timeslots', models.ManyToManyField(to='proposals.TimeSlot', verbose_name='available timeslots', blank=True)),
                ('conference', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='conference', to='conference.Conference')),
                ('creator', models.ForeignKey(verbose_name='creator', to=settings.AUTH_USER_MODEL)),
                ('duration', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='duration', to='conference.SessionDuration')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='type', to='conference.SessionKind')),
            ],
            options={
                'verbose_name': 'proposal version',
                'verbose_name_plural': 'proposal versions',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.CharField(max_length=2, verbose_name='rating', choices=[(b'-1', b'-1'), (b'-0', b'-0'), (b'+0', b'+0'), (b'+1', b'+1')])),
                ('summary', models.TextField(verbose_name='summary')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publication date')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'reviews',
            },
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.PositiveSmallIntegerField(default=0, verbose_name='state', choices=[(0, 'pending request'), (1, 'request accepted'), (2, 'request declined')])),
                ('conference', models.ForeignKey(to='conference.Conference')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'reviewer',
                'verbose_name_plural': 'reviewers',
            },
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('proposals.proposal',),
        ),
        migrations.AddField(
            model_name='review',
            name='proposal',
            field=models.ForeignKey(related_name='reviews', verbose_name='proposal', to='reviews.Proposal'),
        ),
        migrations.AddField(
            model_name='review',
            name='proposal_version',
            field=models.ForeignKey(verbose_name='proposal version', blank=True, to='reviews.ProposalVersion', null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='original',
            field=models.ForeignKey(related_name='versions', verbose_name='original proposal', to='proposals.Proposal'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='speaker',
            field=models.ForeignKey(related_name='proposalversions', on_delete=django.db.models.deletion.PROTECT, verbose_name='speaker', to='speakers.Speaker'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='tags',
            field=pyconde.tagging.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='proposalversion',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='track', blank=True, to='conference.Track', null=True),
        ),
        migrations.AddField(
            model_name='proposalmetadata',
            name='latest_proposalversion',
            field=models.ForeignKey(verbose_name='latest proposal version', blank=True, to='reviews.ProposalVersion', null=True),
        ),
        migrations.AddField(
            model_name='proposalmetadata',
            name='proposal',
            field=models.OneToOneField(related_name='review_metadata', verbose_name='proposal', to='reviews.Proposal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='proposal',
            field=models.ForeignKey(related_name='comments', verbose_name='proposal', to='reviews.Proposal'),
        ),
        migrations.AddField(
            model_name='comment',
            name='proposal_version',
            field=models.ForeignKey(verbose_name='proposal version', blank=True, to='reviews.ProposalVersion', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='reviewer',
            unique_together=set([('conference', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('user', 'proposal')]),
        ),
    ]
