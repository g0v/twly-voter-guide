# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='legislatordetail',
            name='elected_party',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
    ]
