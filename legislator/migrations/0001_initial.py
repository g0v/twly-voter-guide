# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sittings', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100, db_index=True)),
                ('status', models.CharField(max_length=100, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sitting', models.CharField(unique=True, max_length=100)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Legislator',
            fields=[
                ('uid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('former_names', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LegislatorDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ad', models.IntegerField(db_index=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('gender', models.CharField(max_length=100, null=True, blank=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('party', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('caucus', models.CharField(max_length=100, null=True, blank=True)),
                ('constituency', models.IntegerField(db_index=True, null=True, blank=True)),
                ('county', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('district', models.CharField(max_length=100, null=True, blank=True)),
                ('in_office', models.BooleanField(db_index=True)),
                ('contacts', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('term_start', models.DateField(null=True, blank=True)),
                ('term_end', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('education', models.TextField(null=True, blank=True)),
                ('experience', models.TextField(null=True, blank=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('image', models.URLField(null=True, blank=True)),
                ('links', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('platform', models.TextField(null=True, blank=True)),
                ('bill_param', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('vote_param', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('attendance_param', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('legislator', models.ForeignKey(related_name='each_terms', to='legislator.Legislator')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='legislator',
            field=models.ForeignKey(to='legislator.LegislatorDetail'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='sitting',
            field=models.ForeignKey(to='sittings.Sittings'),
        ),
        migrations.AlterUniqueTogether(
            name='legislatordetail',
            unique_together=set([('legislator', 'ad')]),
        ),
    ]
