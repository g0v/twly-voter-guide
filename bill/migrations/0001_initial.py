# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sittings', '__first__'),
        ('legislator', '0002_legislatordetail_elected_party'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('uid', models.TextField(serialize=False, primary_key=True)),
                ('ad', models.IntegerField(db_index=True)),
                ('api_bill_id', models.TextField(unique=True)),
                ('abstract', models.TextField(null=True, blank=True)),
                ('summary', models.TextField(null=True, blank=True)),
                ('bill_type', models.TextField(null=True, blank=True)),
                ('doc', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('proposed_by', models.TextField(null=True, blank=True)),
                ('sitting_introduced', models.TextField(null=True, blank=True)),
                ('last_action_at', models.DateField(db_index=True, null=True, blank=True)),
                ('last_action', models.TextField(db_index=True, null=True, blank=True)),
            ],
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
                ('bill', models.ForeignKey(to='bill.Bill')),
                ('sitting', models.ForeignKey(to='sittings.Sittings')),
            ],
        ),
        migrations.CreateModel(
            name='Legislator_Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priproposer', models.NullBooleanField(db_index=True)),
                ('petition', models.NullBooleanField(db_index=True)),
                ('bill', models.ForeignKey(to='bill.Bill')),
                ('legislator', models.ForeignKey(related_name='bills', to='legislator.LegislatorDetail')),
            ],
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
                ('bill', models.ForeignKey(to='bill.Bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='proposer',
            field=models.ManyToManyField(to='legislator.LegislatorDetail', through='bill.Legislator_Bill'),
        ),
    ]
