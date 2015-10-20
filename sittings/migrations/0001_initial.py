# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sittings',
            fields=[
                ('uid', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('committee', models.TextField(null=True, blank=True)),
                ('date', models.DateField(db_index=True)),
                ('ad', models.PositiveIntegerField()),
                ('session', models.PositiveIntegerField()),
                ('links', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
            ],
        ),
    ]
