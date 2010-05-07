# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Video.reason_disabled'
        db.add_column(u'video', 'reason_disabled', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Video.disabled'
        db.add_column(u'video', 'disabled', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Video.reason_disabled'
        db.delete_column(u'video', 'reason_disabled')

        # Deleting field 'Video.disabled'
        db.delete_column(u'video', 'disabled')
    
    
    models = {
        'bin.bin': {
            'Meta': {'object_name': 'Bin', 'db_table': "u'video_bin'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'writeable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'video.video': {
            'Meta': {'object_name': 'Video', 'db_table': "u'video'"},
            'audio_bitrate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'audio_codec': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'bin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['bin.Bin']"}),
            'channels': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'disabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'encoding': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'encoding_failed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'encoding_status': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'framerate': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {'default': '240'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_hash': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'pixel_aspect_ratio': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'raw_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'reason_disabled': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'samplerate': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'seeding': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sha1': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'still': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'torrent': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'video_bitrate': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'video_codec': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {'default': '320'})
        },
        'video.videohistory': {
            'Meta': {'object_name': 'VideoHistory', 'db_table': "u'video_history'"},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['video.Video']"})
        },
        'video.videoviews': {
            'Meta': {'object_name': 'VideoViews'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'views'", 'to': "orm['video.Video']"})
        }
    }
    
    complete_apps = ['video']
