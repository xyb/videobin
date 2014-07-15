# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings


def render_to_json_response(dictionary, content_type="text/json"):
    indent=None
    if settings.DEBUG:
        content_type = "text/javascript"
        indent = 2
    return HttpResponse(simplejson.dumps(dictionary, indent=indent), content_type=content_type)

def absolute_url(url):
    from django.contrib.sites.models import Site
    return '//%s%s' % (Site.objects.get_current().domain, url)

