# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.contrib import admin

import models


class VideoAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
    list_display = ('title', 'bin', 'created', 'viewed', 'encoding_status')
admin.site.register(models.Video, VideoAdmin)

