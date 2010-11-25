# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.conf.urls.defaults import *
from django.http import HttpResponseNotFound

urlpatterns = patterns('videobin.video.views',
    (r'^.*com.fluendo.player.Cortado', lambda request: HttpResponseNotFound()),
    (r'^.*PortMixerProvider.class', lambda request: HttpResponseNotFound()),
    (r'(?P<binId>.+)/(?P<videoId>.+).iframe.html$', 'iframe'),
    (r'(?P<binId>.+)/(?P<videoId>.+).ogg$', 'video'),
    (r'(?P<binId>.+)/(?P<videoId>.+).html$', 'view'),
    (r'(?P<binId>.+)/(?P<videoId>.+).html.$', 'view'),
    (r'(?P<binId>.+)/(?P<videoId>.+).html..$', 'view'),
    (r'(?P<binId>.+)/(?P<videoId>.+).raw.torrent$', 'raw_torrent'),
    (r'(?P<binId>.+)/(?P<videoId>.+).torrent$', 'torrent'),
    (r'(?P<binId>.+)/(?P<videoId>.+).edit$', 'edit'),
    (r'(?P<binId>.+)/(?P<videoId>.+).chunk$', 'upload'),
    (r'(?P<binId>.+)/(?P<videoId>.+).remove$', 'remove'),
)

urlpatterns += patterns('videobin.bin.views',
    (r'(?P<binId>.+).xml', 'atom'),
    (r'(?P<binId>.+).atom', 'atom'),
    (r'(?P<binId>.+).miro', 'opml'),
    (r'(?P<binId>.+).opml', 'opml'),
    (r'(?P<binId>[a-zA-Z0-9]+)$', 'bin'),
)

