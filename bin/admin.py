# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.contrib import admin

import models


class BinAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
admin.site.register(models.Bin, BinAdmin)

