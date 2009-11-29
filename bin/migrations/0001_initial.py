# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from videobin.bin.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VisitIdentity'
        db.create_table(u'visit_identity', (
            ('id', orm['bin.VisitIdentity:id']),
            ('visit_key', orm['bin.VisitIdentity:visit_key']),
            ('user_id', orm['bin.VisitIdentity:user_id']),
        ))
        db.send_create_signal('bin', ['VisitIdentity'])
        
        # Adding model 'Visit'
        db.create_table(u'visit', (
            ('id', orm['bin.Visit:id']),
            ('visit_key', orm['bin.Visit:visit_key']),
            ('created', orm['bin.Visit:created']),
            ('expiry', orm['bin.Visit:expiry']),
            ('email_address', orm['bin.Visit:email_address']),
        ))
        db.send_create_signal('bin', ['Visit'])
        
        # Adding model 'Bin'
        db.create_table(u'video_bin', (
            ('id', orm['bin.Bin:id']),
            ('title', orm['bin.Bin:title']),
            ('description', orm['bin.Bin:description']),
            ('created', orm['bin.Bin:created']),
            ('updated', orm['bin.Bin:updated']),
            ('writeable', orm['bin.Bin:writeable']),
            ('user_key', orm['bin.Bin:user_key']),
        ))
        db.send_create_signal('bin', ['Bin'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VisitIdentity'
        db.delete_table(u'visit_identity')
        
        # Deleting model 'Visit'
        db.delete_table(u'visit')
        
        # Deleting model 'Bin'
        db.delete_table(u'video_bin')
        
    
    
    models = {
        'bin.bin': {
            'Meta': {'db_table': "u'video_bin'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'writeable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'bin.visit': {
            'Meta': {'db_table': "u'visit'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '765', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visit_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        },
        'bin.visitidentity': {
            'Meta': {'db_table': "u'visit_identity'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'visit_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '120'})
        }
    }
    
    complete_apps = ['bin']
