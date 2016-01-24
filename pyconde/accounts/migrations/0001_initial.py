# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import pyconde.accounts.validators
import pyconde.accounts.managers
import easy_thumbnails.fields
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=256, verbose_name='Username')),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='E-Mail')),
                ('first_name', models.CharField(max_length=30, verbose_name='First name')),
                ('last_name', models.CharField(max_length=30, verbose_name='Last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined')),
                ('short_info', models.TextField(verbose_name='short info', blank=True)),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(validators=[pyconde.accounts.validators.avatar_dimension, pyconde.accounts.validators.avatar_format], upload_to=b'avatars', blank=True, help_text=b'', null=True, verbose_name='avatar')),
                ('num_accompanying_children', models.PositiveIntegerField(default=0, null=True, verbose_name='Number of accompanying children', blank=True)),
                ('age_accompanying_children', models.CharField(max_length=20, verbose_name='Age of accompanying children', blank=True)),
                ('twitter', models.CharField(blank=True, max_length=20, verbose_name='Twitter', validators=[pyconde.accounts.validators.twitter_username])),
                ('website', models.URLField(verbose_name='Website', blank=True)),
                ('organisation', models.TextField(verbose_name='Organisation', blank=True)),
                ('full_name', models.CharField(max_length=255, verbose_name='Full name', blank=True)),
                ('display_name', models.CharField(help_text='What name should be displayed to other people?', max_length=255, verbose_name='Display name', blank=True)),
                ('addressed_as', models.CharField(help_text='How should we call you in mails and dialogs throughout the website?', max_length=255, verbose_name='Address me as', blank=True)),
                ('accept_pysv_conferences', models.BooleanField(default=False, verbose_name='Allow copying to PySV conferences')),
                ('accept_ep_conferences', models.BooleanField(default=False, verbose_name='Allow copying to EPS conferences')),
                ('accept_job_offers', models.BooleanField(default=False, verbose_name='Allow sponsors to send job offers')),
            ],
            options={
                'ordering': ['last_name', 'first_name', 'email'],
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'permissions': (('send_user_mails', 'Allow sending mails to users through the website'), ('export_guidebook', 'Allow export of guidebook data'), ('see_checkin_info', 'Allow seeing check-in information'), ('perform_purchase', 'Allow performing purchases')),
            },
            managers=[
                ('objects', pyconde.accounts.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BadgeStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='badge_status',
            field=models.ManyToManyField(related_name='profiles', verbose_name='Badge status', to='accounts.BadgeStatus', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
