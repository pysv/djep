# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('speakers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightningTalk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slides_url', models.URLField(null=True, verbose_name='slides URL', blank=True)),
                ('speakers', sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='lightning_talks', verbose_name='speakers', to='speakers.Speaker', blank=True)),
            ],
        ),
    ]
