# -*- coding: utf-8 -*-

from south.db import db
from django.db import models
from videobin.video.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VideoViews'
        db.create_table('video_videoviews', (
            ('id', orm['video.VideoViews:id']),
            ('video', orm['video.VideoViews:video']),
            ('date', orm['video.VideoViews:date']),
        ))
        db.send_create_signal('video', ['VideoViews'])
        
        # Adding model 'VideoHistory'
        db.create_table(u'video_history', (
            ('id', orm['video.VideoHistory:id']),
            ('video', orm['video.VideoHistory:video']),
            ('title', orm['video.VideoHistory:title']),
            ('description', orm['video.VideoHistory:description']),
            ('date', orm['video.VideoHistory:date']),
        ))
        db.send_create_signal('video', ['VideoHistory'])
        
        # Adding model 'Video'
        db.create_table(u'video', (
            ('id', orm['video.Video:id']),
            ('title', orm['video.Video:title']),
            ('description', orm['video.Video:description']),
            ('created', orm['video.Video:created']),
            ('updated', orm['video.Video:updated']),
            ('bin', orm['video.Video:bin']),
            ('encoding', orm['video.Video:encoding']),
            ('encoding_failed', orm['video.Video:encoding_failed']),
            ('encoding_status', orm['video.Video:encoding_status']),
            ('seeding', orm['video.Video:seeding']),
            ('sha1', orm['video.Video:sha1']),
            ('duration', orm['video.Video:duration']),
            ('size', orm['video.Video:size']),
            ('info_hash', orm['video.Video:info_hash']),
            ('video_codec', orm['video.Video:video_codec']),
            ('video_bitrate', orm['video.Video:video_bitrate']),
            ('framerate', orm['video.Video:framerate']),
            ('width', orm['video.Video:width']),
            ('height', orm['video.Video:height']),
            ('pixel_aspect_ratio', orm['video.Video:pixel_aspect_ratio']),
            ('audio_codec', orm['video.Video:audio_codec']),
            ('audio_bitrate', orm['video.Video:audio_bitrate']),
            ('samplerate', orm['video.Video:samplerate']),
            ('channels', orm['video.Video:channels']),
            ('file', orm['video.Video:file']),
            ('raw_file', orm['video.Video:raw_file']),
            ('torrent', orm['video.Video:torrent']),
            ('still', orm['video.Video:still']),
            ('done', orm['video.Video:done']),
        ))
        db.send_create_signal('video', ['Video'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VideoViews'
        db.delete_table('video_videoviews')
        
        # Deleting model 'VideoHistory'
        db.delete_table(u'video_history')
        
        # Deleting model 'Video'
        db.delete_table(u'video')
        
    
    
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
        'video.video': {
            'Meta': {'db_table': "u'video'"},
            'audio_bitrate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'audio_codec': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'bin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['bin.Bin']"}),
            'channels': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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
            'Meta': {'db_table': "u'video_history'"},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': "orm['video.Video']"})
        },
        'video.videoviews': {
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'views'", 'to': "orm['video.Video']"})
        }
    }
    
    complete_apps = ['video']
