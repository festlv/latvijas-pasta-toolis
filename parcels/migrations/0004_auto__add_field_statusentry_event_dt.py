# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StatusEntry.event_dt'
        db.add_column(u'parcels_statusentry', 'event_dt',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 20, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StatusEntry.event_dt'
        db.delete_column(u'parcels_statusentry', 'event_dt')


    models = {
        u'parcels.shipment': {
            'Meta': {'object_name': 'Shipment'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_check_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '13'})
        },
        u'parcels.statusentry': {
            'Meta': {'object_name': 'StatusEntry'},
            'created_dt': ('django.db.models.fields.DateTimeField', [], {}),
            'event_dt': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shipment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parcels.Shipment']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['parcels']