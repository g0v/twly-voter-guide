# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standpoint', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_standpoint',
            name='opinion',
        ),
        migrations.AddField(
            model_name='standpoint',
            name='pro',
            field=models.IntegerField(default=0),
        ),
    ]
