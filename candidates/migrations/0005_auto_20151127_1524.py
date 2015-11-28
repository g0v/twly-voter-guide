# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0004_auto_20151126_0855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terms',
            name='latest_term',
            field=models.ForeignKey(blank=True, to='legislator.LegislatorDetail', null=True),
        ),
    ]
