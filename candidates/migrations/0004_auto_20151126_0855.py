# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('legislator', '0002_legislatordetail_elected_party'),
        ('candidates', '0003_auto_20151112_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.CharField(max_length=70, serialize=False, primary_key=True)),
                ('ad', models.IntegerField(db_index=True)),
                ('number', models.IntegerField(db_index=True, null=True, blank=True)),
                ('priority', models.IntegerField(db_index=True, null=True, blank=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100, null=True, blank=True)),
                ('party', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('constituency', models.IntegerField(db_index=True)),
                ('county', models.CharField(max_length=100, db_index=True)),
                ('district', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('votes', models.IntegerField(null=True, blank=True)),
                ('votes_percentage', models.CharField(max_length=100, null=True, blank=True)),
                ('elected', models.NullBooleanField(db_index=True)),
                ('contact_details', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('education', models.TextField(null=True, blank=True)),
                ('experience', models.TextField(null=True, blank=True)),
                ('remark', models.TextField(null=True, blank=True)),
                ('image', models.URLField(null=True, blank=True)),
                ('links', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
                ('platform', models.TextField(null=True, blank=True)),
                ('politicalcontributions', json_field.fields.JSONField(default='null', help_text='Enter a valid JSON object', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='candidates',
            name='former_names',
            field=django.contrib.postgres.fields.ArrayField(default=None, null=True, base_field=models.CharField(max_length=100), size=None),
        ),
        migrations.AlterUniqueTogether(
            name='candidates',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='candidates',
            index_together=set([]),
        ),
        migrations.AddField(
            model_name='terms',
            name='candidate',
            field=models.ForeignKey(to='candidates.Candidates'),
        ),
        migrations.AddField(
            model_name='terms',
            name='latest_term',
            field=models.OneToOneField(null=True, blank=True, to='legislator.LegislatorDetail'),
        ),
        migrations.AddField(
            model_name='terms',
            name='legislator',
            field=models.OneToOneField(related_name='elected_candidate', null=True, blank=True, to='legislator.LegislatorDetail'),
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='ad',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='constituency',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='contact_details',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='county',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='district',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='education',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='elected',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='image',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='latest_term',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='legislator',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='links',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='number',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='party',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='platform',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='politicalcontributions',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='remark',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='votes',
        ),
        migrations.RemoveField(
            model_name='candidates',
            name='votes_percentage',
        ),
        migrations.AlterIndexTogether(
            name='terms',
            index_together=set([('ad', 'county', 'constituency')]),
        ),
    ]
