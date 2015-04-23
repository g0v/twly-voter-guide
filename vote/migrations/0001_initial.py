# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sittings', '__first__'),
        ('legislator', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Legislator_Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('decision', models.IntegerField(db_index=True, null=True, blank=True)),
                ('conflict', models.NullBooleanField(db_index=True)),
                ('legislator', models.ForeignKey(related_name='votes', to='legislator.LegislatorDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('uid', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('vote_seq', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=100, null=True, blank=True)),
                ('content', models.TextField()),
                ('conflict', models.NullBooleanField()),
                ('result', models.CharField(max_length=50, null=True, blank=True)),
                ('results', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('sitting', models.ForeignKey(related_name='votes', to='sittings.Sittings')),
                ('voter', models.ManyToManyField(to='legislator.LegislatorDetail', through='vote.Legislator_Vote')),
            ],
        ),
        migrations.AddField(
            model_name='legislator_vote',
            name='vote',
            field=models.ForeignKey(to='vote.Vote'),
        ),
    ]
