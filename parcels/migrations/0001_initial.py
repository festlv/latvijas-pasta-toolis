# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shipment'
        db.create_table(u'parcels_shipment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tracking_number', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('last_check_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_dt', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'parcels', ['Shipment'])

        # Adding model 'StatusEntry'
        db.create_table(u'parcels_statusentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_dt', self.gf('django.db.models.fields.DateTimeField')()),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('shipment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parcels.Shipment'])),
        ))
        db.send_create_signal(u'parcels', ['StatusEntry'])


    def backwards(self, orm):
        # Deleting model 'Shipment'
        db.delete_table(u'parcels_shipment')

        # Deleting model 'StatusEntry'
        db.delete_table(u'parcels_statusentry')


    models = {
        u'parcels.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'created_dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_check_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '13'})
        },
        u'parcels.statusentry': {
            'Meta': {'object_name': 'StatusEntry'},
            'created_dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parcels.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['parcels']