# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_auto_20141211_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legislator_vote',
            name='conflict',
            field=models.NullBooleanField(db_index=True),
            preserve_default=True,
        ),
    ]
