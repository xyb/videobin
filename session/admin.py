# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.contrib import admin

import models


class UserSettingsAdmin(admin.ModelAdmin):
    search_fields = ['email_address', 'user_key']
    list_display = ('user_key', 'email_address')
admin.site.register(models.UserSettings, UserSettingsAdmin)

