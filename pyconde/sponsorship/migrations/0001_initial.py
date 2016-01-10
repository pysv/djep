# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('text', models.TextField(verbose_name='Text')),
                ('link', models.URLField(verbose_name='URL')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('sponsor__level__order', '-added'),
                'verbose_name': 'Job offer',
                'verbose_name_plural': 'Job offers',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('external_url', models.URLField(verbose_name='external URL')),
                ('annotation', models.TextField(verbose_name='annotation', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('contact_name', models.CharField(max_length=100, null=True, verbose_name='contact_name', blank=True)),
                ('contact_email', models.EmailField(max_length=254, null=True, verbose_name='Contact e\u2011mail', blank=True)),
                ('logo', models.ImageField(upload_to=b'sponsor_logos/', verbose_name='logo')),
                ('added', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added')),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('custom_logo_size_listing', models.CharField(help_text='Format: [width]x[height]. To get the maximum height out of a logo, use something like 300x55.', max_length=9, null=True, verbose_name='Custom logo size in listings', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'sponsor',
                'verbose_name_plural': 'sponsors',
            },
        ),
        migrations.CreateModel(
            name='SponsorLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('order', models.IntegerField(default=0, verbose_name='order')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('slug', models.SlugField(verbose_name='slug')),
                ('conference', models.ForeignKey(verbose_name='conference', to='conference.Conference')),
            ],
            options={
                'ordering': ['conference', 'order'],
                'verbose_name': 'sponsor level',
                'verbose_name_plural': 'sponsor levels',
            },
        ),
        migrations.CreateModel(
            name='SponsorListPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=100, verbose_name='title', blank=True)),
                ('group', models.BooleanField(default=False, verbose_name='group by level')),
                ('split_list_length', models.IntegerField(default=None, null=True, verbose_name='length of split splits', blank=True)),
                ('custom_css_classes', models.CharField(help_text='Use slides-2rows if your row actually consists of two rows.', max_length=100, verbose_name='custom CSS classes', blank=True)),
                ('levels', models.ManyToManyField(to='sponsorship.SponsorLevel', verbose_name='sponsor levels')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='level',
            field=models.ForeignKey(verbose_name='level', to='sponsorship.SponsorLevel'),
        ),
        migrations.AddField(
            model_name='joboffer',
            name='sponsor',
            field=models.ForeignKey(verbose_name='sponsor', to='sponsorship.Sponsor'),
        ),
    ]
