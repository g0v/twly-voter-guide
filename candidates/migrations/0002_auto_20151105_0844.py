# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidates',
            name='latest_term',
            field=models.OneToOneField(null=True, blank=True, to='legislator.LegislatorDetail'),
        ),
        migrations.AlterField(
            model_name='candidates',
            name='legislator',
            field=models.OneToOneField(related_name='elected_candidate', null=True, blank=True, to='legislator.LegislatorDetail'),
        ),
    ]
