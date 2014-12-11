# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='hits',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='summary',
        ),
    ]
