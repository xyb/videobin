# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from datetime import datetime

from django.contrib.sites.models import Site
from django.template import Library, Node
from django.template.defaultfilters import stringfilter

from oxlib import formatDuration

register = Library()

@register.filter
def with_domain(url):
    return 'http://%s%s' % (Site.objects.get_current().domain, url) 

@register.filter
def format_since(d):
    since = datetime.now() - d
    if not since.days:
        if since.seconds < 60:
            return formatDuration(1000 * since.seconds, verbosity=2) + " ago"
        else:
            return formatDuration(1000 * int(since.seconds / 60) * 60, verbosity=2) + " ago"
    return d.strftime('%Y-%m-%d %H:%M')


@register.filter
@stringfilter
def is_autoplay(embed, autoplay):
    if not autoplay:
        embed = embed.replace('iframe.html', 'iframe.html?autoplay=0')
    return embed

