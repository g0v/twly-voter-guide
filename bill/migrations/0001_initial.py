# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('legislator', '__first__'),
        ('sittings', '0002_sittings_links'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uid', models.TextField(unique=True)),
                ('api_bill_id', models.TextField(unique=True)),
                ('abstract', models.TextField(null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('bill_type', models.TextField(null=True, blank=True)),
                ('doc', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('proposed_by', models.TextField(null=True, blank=True)),
                ('sitting_introduced', models.TextField(null=True, blank=True)),
                ('last_action_at', models.DateField(null=True, blank=True)),
                ('last_action', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillMotions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agenda_item', models.IntegerField(null=True, blank=True)),
                ('committee', models.TextField(null=True, blank=True)),
                ('item', models.TextField(null=True, blank=True)),
                ('motion_class', models.TextField(null=True, blank=True)),
                ('resolution', models.TextField(null=True, blank=True)),
                ('status', models.TextField(null=True, blank=True)),
                ('bill', models.ForeignKey(to='bill.Bill', to_field=b'uid')),
                ('sitting', models.ForeignKey(to='sittings.Sittings', to_field=b'uid')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Legislator_Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priproposer', models.NullBooleanField()),
                ('petition', models.NullBooleanField()),
                ('bill', models.ForeignKey(to='bill.Bill', to_field=b'uid')),
                ('legislator', models.ForeignKey(blank=True, to='legislator.LegislatorDetail', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ttsMotions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sitting_id', models.TextField(null=True, blank=True)),
                ('agencies', models.TextField(null=True, blank=True)),
                ('category', models.TextField(null=True, blank=True)),
                ('chair', models.TextField(null=True, blank=True)),
                ('date', models.DateField()),
                ('memo', models.TextField(null=True, blank=True)),
                ('motion_type', models.TextField(null=True, blank=True)),
                ('progress', models.TextField(null=True, blank=True)),
                ('resolution', models.TextField(null=True, blank=True)),
                ('source', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('speakers', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('tags', models.TextField(null=True, blank=True)),
                ('topic', models.TextField(null=True, blank=True)),
                ('tts_key', models.TextField(null=True, blank=True)),
                ('bill', models.ForeignKey(to='bill.Bill', to_field=b'uid')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bill',
            name='proposer',
            field=models.ManyToManyField(to='legislator.LegislatorDetail', null=True, through='bill.Legislator_Bill', blank=True),
            preserve_default=True,
        ),
    ]
