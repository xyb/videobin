# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.db import models
from ox import to36

from videobin.utils.shortcuts import absolute_url


class Visit(models.Model):
    visit_key = models.CharField(unique=True, max_length=120)
    created = models.DateTimeField(null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    email_address = models.CharField(max_length=765, blank=True)
    class Meta:
        db_table = u'visit'

class VisitIdentity(models.Model):
    visit_key = models.CharField(unique=True, max_length=120)
    user_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'visit_identity'

class Bin(models.Model):
    title = models.CharField(blank=True, max_length=1000)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    writeable = models.BooleanField(default=False)
    #FIXME:
    #uploader = models.ForeignKey(Visit, related_name='bins', default=None)
    user_key = models.CharField(max_length=40, blank=True)

    class Meta:
        db_table = u'video_bin'

    def __unicode__(self):
        return "%s" % self.title

    def hID(self):
        return to36(self.id)

    def get_absolute_url(self):
        return "/+%s" % self.hID()

    def atomLink(self):
        return absolute_url("%s.xml" % self.get_absolute_url())

    def miroLink(self):
        return absolute_url("%s.miro" % self.get_absolute_url())

    def videoInfo(self):
        videos = self.videos.all().count()
        r = "%s Video" % videos
        if videos != 1:
            r += "s"
        return r

