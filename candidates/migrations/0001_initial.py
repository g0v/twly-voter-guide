# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('legislator', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ad', models.IntegerField(db_index=True)),
                ('number', models.IntegerField(db_index=True, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('birth', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(max_length=100, null=True, blank=True)),
                ('party', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('constituency', models.IntegerField(db_index=True)),
                ('county', models.CharField(max_length=100, db_index=True)),
                ('district', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('votes', models.IntegerField(null=True, blank=True)),
                ('elected', models.NullBooleanField(db_index=True)),
                ('contact_details', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('education', models.TextField(null=True, blank=True)),
                ('experience', models.TextField(null=True, blank=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('image', models.URLField(null=True, blank=True)),
                ('links', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('platform', models.TextField(null=True, blank=True)),
                ('legislator', models.ForeignKey(blank=True, to='legislator.LegislatorDetail', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
