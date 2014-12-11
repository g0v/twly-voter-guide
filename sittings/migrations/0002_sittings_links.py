# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sittings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sittings',
            name='links',
            field=json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True),
            preserve_default=True,
        ),
    ]
