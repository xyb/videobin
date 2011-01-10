# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

import os
from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

from ox import to36, formatDuration, formatBytes, avinfo, createTorrent
import ox.torrent

from videobin.bin.models import Bin

from theoraenc import TheoraEnc
import transmission


def absolute_url(url):
    from django.contrib.sites.models import Site
    return 'http://%s%s' % (Site.objects.get_current().domain, url) 

def video_name(video, filename):
    hid = to36(video.id)
    video = "%s/%s.ogg" %(hid[0], hid)
    return video

class Video(models.Model):
    title = models.CharField(blank=True, max_length=1000)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    bin = models.ForeignKey(Bin, related_name='videos')
    encoding = models.BooleanField(default=False)
    encoding_failed = models.BooleanField(default=False)
    encoding_status = models.CharField(blank=True, max_length=1000)
    seeding = models.BooleanField(default=False)
    sha1 = models.CharField(max_length=120, blank=True)
    duration = models.IntegerField(default=-1)
    size = models.BigIntegerField(default=-1)
    info_hash = models.CharField(blank=True, max_length=40)
    video_codec = models.CharField(blank=True, max_length=200)
    video_bitrate = models.CharField(blank=True, max_length=200)
    framerate = models.CharField(blank=True, max_length=200)
    width = models.IntegerField(default=320)
    height = models.IntegerField(default=240)
    pixel_aspect_ratio = models.CharField(blank=True, max_length=200, default='')
    audio_codec = models.CharField(blank=True, max_length=200, default='')
    audio_bitrate = models.CharField(blank=True, max_length=200, default='')
    samplerate = models.IntegerField(default=-  1)
    channels = models.IntegerField(default=-1)
    file = models.FileField(upload_to=video_name, blank=True)
    raw_file = models.FileField(upload_to=lambda v, f: video_name(v, f) + '.upload', blank=True)
    torrent = models.FileField(upload_to=lambda v, f: video_name(v, f) + '.torrent', blank=True)
    raw_torrent = models.FileField(upload_to=lambda v, f: video_name(v, f) + '.raw.torrent', blank=True, null=True)
    still = models.FileField(upload_to=lambda v, f: video_name(v, f).replace('.ogg', '.jpg'), blank=True)
    done = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    reason_disabled = models.TextField(blank=True, default='')


    class Meta:
        db_table = u'video'

    def save(self, *args, **kwargs):
        self.bin.updated = datetime.now()
        self.bin.save()
        super(Video, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        transmission.removeTorrent(self.info_hash)
        super(Video, self).delete(*args, **kwargs)

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.bin.title)

    def save_chunk(self, chunk, name='video.ogv'):
        if not self.done:
            if not self.file:
                self.file.save(name, ContentFile(chunk))
                self.title = os.path.splitext(os.path.basename(name))[0]
                if self.bin.title == '___title___':
                    self.bin.title = self.title
                    self.bin.save()
                self.save()
            else:
                f = open(self.file.path, 'a')
                f.write(chunk)
                f.close()
            return True
        return False

    def linkBase(self):
        return "%s/%s" % (self.bin.get_absolute_url(), to36(self.id))

    def get_absolute_url(self):
        url = "%s.html" % self.linkBase()
        return absolute_url(url)

    def editLink(self):
        url = "%s.edit" % self.linkBase()
        return absolute_url(url)

    def torrentLink(self):
        url = "%s.torrent" % self.linkBase()
        return absolute_url(url)

    def rawTorrentLink(self):
        url = "%s.raw.torrent" % self.linkBase()
        return absolute_url(url)

    def videoLink(self):
        url = "%s.ogg" % self.linkBase()
        return absolute_url(url)

    def staticVideoLink(self):
        #FIXME: why is MEDIA_URL ignored?
        return absolute_url(self.file.url)

    def embedElement(self):
        url = "%s.iframe.html" % self.linkBase()
        url = absolute_url(url)
        embed = '<iframe src="%s" width="%s" height="%s" frameborder="0" scrolling="no"></iframe>' % \
                (url, self.displayWidth(), self.displayHeight())
        return embed

    def displayHeight(self):
        h = self.height
        if float(self.width) / h < 1.5:
          h = min(h, 336)
        else:
          h = min(h, 288)
        return h

    def displayWidth(self):
        w = self.width
        if float(w) / self.height < 1.5:
          w = min(w, 448)
        else:
          w = min(w, 512)
        return w

    def formatInfoHtml(self):
        info = ''
        codec_info = self.video_codec
        if self.audio_codec:
          codec_info += "/" + self.audio_codec
        codec_info = "%sx%s (%s)" % (self.width, self.height, codec_info)
        if not self.video_codec:
          codec_info = self.audio_codec

        info += "%s .:. %s .:. %s" % \
          (formatDuration(self.duration, milliseconds=False), formatBytes(self.size),
           codec_info)
        if self.duration < 0 or self.encoding:
          return ''
        return info

    def downloadFilename(self):
        fname = "%s.ogg" % self.title.replace(' ', '_')
        fname = fname.replace('.ogg.ogg', '.ogg')
        return fname

    def loadMetadata(self):
        if not self.file and self.raw_file and os.path.exists(self.raw_file.path):
            self.encoding = True
            self.save()
            return
        os.chmod(self.file.path,0644)
        d = avinfo(self.file.path)
        if 'audio' not in d and 'video' not in d:
            if not self.raw_file and os.path.exists(self.file.path):
                self.raw_file.name = self.file.name + '.upload'
                os.rename(self.file.path, self.raw_file.path)
                self.encoding = True
                self.save()
                return
        #Update DB
        if 'title' in d and self.title:
            del d['title']
        #FIXME:
        for key in ('duration', 'oshash', 'size'):
            if key in d:
                value = d[key]
                if key == 'duration':
                    value = float(value) * 1000   
                setattr(self, key, value)
        if d['video']:
            for key in ('width', 'height', 'framerate'):
                if key in d['video'][0]:
                    setattr(self, key, d['video'][0][key])
            self.video_codec = d['video'][0]['codec'].capitalize()
        if d['audio']:
            for key in ('channels', 'samplerate'):
                if key in d['audio'][0]:
                    setattr(self, key, d['audio'][0][key])
            self.audio_codec = d['audio'][0]['codec'].capitalize()

        #FIXME: check for to big ogg files here and initiate transcoding
        #base = os.path.dirname(__file__)
        #cmd = '''%s/bin/extract_still.py "%s" "%s" %s''' % (base, self.file.path, self.still.path, self.duration / 2)
        #os.system(cmd)

        self.createTorrent()
        self.encoding = False
        self.save()

    def createTorrent(self):
        self.torrent.name = video_name(self, "") + ".torrent"
        self.save()
        cfg = dict(
            target=self.torrent.path,
            comment=settings.TORRENT_COMMENT,
        )
        createTorrent(self.file.path, settings.ANNOUNCE_URL, cfg)
        self.info_hash = ox.torrent.getInfoHash(self.torrent.path)
        self.save()
        transmission.addTorrent(self.torrent.path)
        if settings.SHARE_RAW_TORRENT:
            self.raw_torrent.name = video_name(self, "") + ".raw.torrent"
            self.save()
            cfg = dict(
                target=self.raw_torrent.path,
                comment=settings.TORRENT_COMMENT,
            )
            createTorrent(self.raw_file.path, settings.ANNOUNCE_URL, cfg)
            if settings.SEED_RAW_TORRENT:
                transmission.addTorrent(self.raw_torrent.path)

    def encode(self):
        inputFile = self.raw_file.path
        self.file.name = video_name(self, "video.ogv")
        outputFile = self.file.path
        _enc = TheoraEnc(inputFile, outputFile)
        if _enc.encode():
          self.loadMetadata()
        else:
          self.encoding_status = "Encoding Failed."
          self.encoding = True
          self.encoding_failed = True
          self.save()

    def viewed(self):
        return self.views.all().count()

class VideoViews(models.Model):
    video = models.ForeignKey(Video, related_name='views')
    date = models.DateTimeField(auto_now_add=True)

class VideoHistory(models.Model):
    video = models.ForeignKey(Video, related_name='history')
    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'video_history'

