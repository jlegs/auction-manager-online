# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field attendee on 'MergedInvoice'
        db.delete_table(db.shorten_name(u'manager_mergedinvoice_attendee'))


    def backwards(self, orm):
        # Adding M2M table for field attendee on 'MergedInvoice'
        m2m_table_name = db.shorten_name(u'manager_mergedinvoice_attendee')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mergedinvoice', models.ForeignKey(orm['manager.mergedinvoice'], null=False)),
            ('attendee', models.ForeignKey(orm['manager.attendee'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mergedinvoice_id', 'attendee_id'])


    models = {
        'manager.attendee': {
            'Meta': {'object_name': 'Attendee'},
            'bid_number': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'table_assignment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2014'})
        },
        'manager.auctionitem': {
            'Meta': {'object_name': 'AuctionItem'},
            'date_received': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 2, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'increment_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '2'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'items'", 'null': 'True', 'blank': 'True', 'to': "orm['manager.Invoice']"}),
            'item_number': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'retail_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '2'}),
            'selling_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'null': 'True', 'max_digits': '30', 'decimal_places': '2', 'blank': 'True'}),
            'starting_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '30', 'decimal_places': '2'}),
            'winning_bid_number': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2014'})
        },
        'manager.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'attendee': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'invoice'", 'null': 'True', 'default': 'None', 'to': "orm['manager.Attendee']", 'blank': 'True', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 2, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'merged_invoice': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'invoices'", 'null': 'True', 'blank': 'True', 'to': "orm['manager.MergedInvoice']"}),
            'paid_for_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'invoices_paid'", 'null': 'True', 'blank': 'True', 'to': "orm['manager.Attendee']"}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2014'})
        },
        'manager.mergedinvoice': {
            'Meta': {'object_name': 'MergedInvoice'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 6, 2, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'paid_for_by': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'merged_invoices_paid'", 'null': 'True', 'blank': 'True', 'to': "orm['manager.Attendee']"}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2014'})
        }
    }

    complete_apps = ['manager']