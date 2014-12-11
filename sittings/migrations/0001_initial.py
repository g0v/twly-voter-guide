# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sittings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('committee', models.TextField(null=True, blank=True)),
                ('date', models.DateField()),
                ('ad', models.IntegerField()),
                ('session', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
