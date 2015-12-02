# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_auto_20151127_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='terms',
            name='councilor',
            field=json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True),
        ),
    ]
