# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

import os
import time
import base64

import transmissionrpc
import ox.torrent
from django.conf import settings

import models


DEBUG = False

def connect():
    return transmissionrpc.Client(settings.TRANSMISSON_HOST,
                                  port=settings.TRANSMISSON_PORT,
                                  user=settings.TRANSMISSON_USER,
                                  password=settings.TRANSMISSON_PASSWORD)

def removeTorrent(info_hash):
    if DEBUG:
        print 'remove', info_hash
    if info_hash:
        try:
            tc = connect()
            tc.remove(info_hash.lower())
        except:
            if DEBUG:
                import traceback
                traceback.print_exc()
        
def addTorrent(torrent_file):
    download_dir = os.path.dirname(torrent_file)
    f = open(torrent_file)
    torrent_data = base64.b64encode(f.read())
    f.close()
    info_hash = ox.torrent.get_info_hash(torrent_file)
    try:
        tc = connect()
        if not isSeeding(info_hash):
            tc.add(torrent_data, download_dir=download_dir)
    except:
        if DEBUG:
            import traceback
            traceback.print_exc()

def isSeeding(info_hash):
    info_hash = info_hash.lower()
    try:
        tc = connect()
        torrents = tc.info(info_hash)
    except:
        torrents = False
        if DEBUG:
            import traceback
            traceback.print_exc()
    if torrents:
        return True
    return False

def seedAllVideos():
    tc = connect()
    for v in models.Video.objects.filter(done=True,
                                         encoding=False,
                                         encoding_failed=False):
        if v.torrent and os.path.exists(v.torrent.path):
            if DEBUG:
                print "add", v.torrent.path
            addTorrent(v.torrent.path)

def startDaemon():
    from subprocess import Popen
    try:
        tc = connect()
    except:
        Popen(['transmission-daemon',
            '-a', '127.0.0.1',
            '-r', '127.0.0.1',
            '-p', str(settings.TRANSMISSON_PORT),
            '--auth',
            '-u', settings.TRANSMISSON_USER,
            '-v', settings.TRANSMISSON_PASSWORD,
            '-w', settings.MEDIA_ROOT,
        ])
        time.sleep(1)

