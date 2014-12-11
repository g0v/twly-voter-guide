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
                ('decision', models.IntegerField(null=True, blank=True)),
                ('conflict', models.NullBooleanField()),
                ('legislator', models.ForeignKey(related_name='votes', to='legislator.LegislatorDetail')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.CharField(unique=True, max_length=110)),
                ('vote_seq', models.CharField(max_length=10)),
                ('category', models.CharField(max_length=100, null=True, blank=True)),
                ('content', models.TextField()),
                ('summary', models.TextField(null=True, blank=True)),
                ('hits', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('conflict', models.NullBooleanField()),
                ('result', models.CharField(max_length=50, null=True, blank=True)),
                ('results', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('sitting', models.ForeignKey(related_name='votes', to='sittings.Sittings', to_field=b'uid')),
                ('voter', models.ManyToManyField(to='legislator.LegislatorDetail', through='vote.Legislator_Vote')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='legislator_vote',
            name='vote',
            field=models.ForeignKey(to='vote.Vote', to_field=b'uid'),
            preserve_default=True,
        ),
    ]
