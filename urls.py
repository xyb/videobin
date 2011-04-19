# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from django.conf.urls.defaults import *
from django.shortcuts import render_to_response

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^\+', include('videobin.bin.urls')),

    (r'^$', "videobin.bin.views.index"),
    (r'^help$', "videobin.views.help"),
    (r'^help/encoding$', "videobin.views.help_encoding"),
    (r'^bins$', "videobin.bin.views.bins"),
    (r'^about$', "videobin.views.about"),
    (r'^code$', "videobin.views.code"),
    (r'^api$', "videobin.views.api"),
    (r'^feedback$', "videobin.views.feedback"),
    (r'^feedback/thanks$', "videobin.views.feedback_thanks"),
    (r'^add$', "videobin.video.views.add"),
    (r'^r/(?P<key>.*)$', "videobin.session.views.recover"),
    (r'^recover/post$', "videobin.session.views.recover_request"),
    (r'^recover$', "videobin.session.views.recover_sent"),
    (r'^recover/failed$', "videobin.session.views.recover_failed"),
    (r'^settings$', "videobin.session.views.settings"),
    (r'^progress$', "videobin.views.upload_progress"),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
                               'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )


