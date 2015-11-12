# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0002_auto_20151105_0844'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='candidates',
            index_together=set([('ad', 'county', 'constituency')]),
        ),
    ]
