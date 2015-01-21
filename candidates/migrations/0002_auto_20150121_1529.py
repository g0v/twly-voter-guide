# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislator', '__first__'),
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidates',
            name='latest_term',
            field=models.ForeignKey(blank=True, to='legislator.LegislatorDetail', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='candidates',
            name='legislator',
            field=models.ForeignKey(related_name='elected_candidate', blank=True, to='legislator.LegislatorDetail', null=True),
            preserve_default=True,
        ),
    ]
