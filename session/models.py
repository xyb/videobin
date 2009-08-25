# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.db import models


class UserSettings(models.Model):
    user_key = models.CharField(unique=True, max_length=60)
    email_address = models.CharField(max_length=765, blank=True)

def getUserSettings(user_key):
    try:
        settings = UserSettings.objects.get(user_key=user_key)
    except UserSettings.DoesNotExist:
        settings = UserSettings.objects.create(user_key=user_key)
        settings.save()
    return settings

