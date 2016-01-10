# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sessions_attending',
            field=models.ManyToManyField(related_name='attendees', verbose_name='Trainings', to='schedule.Session', blank=True),
        ),
    ]
