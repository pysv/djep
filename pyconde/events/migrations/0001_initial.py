# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conference', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='End date', blank=True)),
                ('link', models.URLField(null=True, verbose_name='Link', blank=True)),
                ('conference', models.ForeignKey(verbose_name='Conference', to='conference.Conference')),
            ],
            options={
                'ordering': ['date'],
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
    ]
