# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='legislator_vote',
            unique_together=set([('legislator', 'vote')]),
        ),
    ]
