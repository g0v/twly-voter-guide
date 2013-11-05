# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Legislator'
        db.create_table(u'legislator_legislator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('eleDistrict', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('districtDetail', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('committee', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('enable', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('enableSession', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('enabledate', self.gf('django.db.models.fields.DateField')(null=True)),
            ('disableReason', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('hits', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('wiki', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('officialsite', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'legislator', ['Legislator'])

        # Adding model 'Politics'
        db.create_table(u'legislator_politics', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('legislator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legislator.Legislator'], null=True)),
            ('politic', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('category', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('party', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'legislator', ['Politics'])

        # Adding model 'FileLog'
        db.create_table(u'legislator_filelog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'legislator', ['FileLog'])

        # Adding model 'Attendance'
        db.create_table(u'legislator_attendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('legislator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['legislator.Legislator'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sessionPrd', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('session', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('category', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('presentNum', self.gf('django.db.models.fields.IntegerField')()),
            ('unpresentNum', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'legislator', ['Attendance'])


    def backwards(self, orm):
        # Deleting model 'Legislator'
        db.delete_table(u'legislator_legislator')

        # Deleting model 'Politics'
        db.delete_table(u'legislator_politics')

        # Deleting model 'FileLog'
        db.delete_table(u'legislator_filelog')

        # Deleting model 'Attendance'
        db.delete_table(u'legislator_attendance')


    models = {
        u'legislator.attendance': {
            'Meta': {'object_name': 'Attendance'},
            'category': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legislator.Legislator']"}),
            'presentNum': ('django.db.models.fields.IntegerField', [], {}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sessionPrd': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'unpresentNum': ('django.db.models.fields.IntegerField', [], {})
        },
        u'legislator.filelog': {
            'Meta': {'object_name': 'FileLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'session': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'legislator.legislator': {
            'Meta': {'object_name': 'Legislator'},
            'committee': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'disableReason': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'districtDetail': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'eleDistrict': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'enable': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'enableSession': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'enabledate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'hits': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'officialsite': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'wiki': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'legislator.politics': {
            'Meta': {'object_name': 'Politics'},
            'category': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legislator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['legislator.Legislator']", 'null': 'True'}),
            'party': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'politic': ('django.db.models.fields.TextField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['legislator']