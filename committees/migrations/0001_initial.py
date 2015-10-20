# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legislator', '0002_legislatordetail_elected_party'),
    ]

    operations = [
        migrations.CreateModel(
            name='Committees',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('category', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Legislator_Committees',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ad', models.IntegerField()),
                ('session', models.IntegerField()),
                ('chair', models.BooleanField()),
                ('committee', models.ForeignKey(to='committees.Committees', to_field=b'name')),
                ('legislator', models.ForeignKey(to='legislator.LegislatorDetail')),
            ],
        ),
        migrations.AddField(
            model_name='committees',
            name='members',
            field=models.ManyToManyField(to='legislator.LegislatorDetail', through='committees.Legislator_Committees'),
        ),
    ]
