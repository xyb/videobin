# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2011 by j@mailb.org

from django.core.management.base import BaseCommand 

class Command(BaseCommand):
    """
    """
    help = 'migrate views into video table, only required to run once.'
    args = ''

    def handle(self, **options):
        from videobin.video import models
        from django.db.models import F
        if models.VideoViews.objects.all().count() > 0:
            for v in models.Video.objects.all():
                models.Video.objects.filter(pk=v.id).update(
                        viewed=F('viewed')+v.views.all().count())
                v.views.all().delete()
        else:
            print 'no views left to migrate'

