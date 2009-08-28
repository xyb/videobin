# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    """
    background loop encoding videos.
    """
    help = 'encode videos in queue.'
    args = ''

    def handle(self, **options):
        from videobin.video.models import Video
        for video in Video.objects.filter(done=True, encoding=True, encoding_failed=False):
            video.encode()

