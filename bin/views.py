# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.utils import feedgenerator
#fixme use that instead of writing it on my own
#from webapi.utils.feedgenerator import Thumbnail, Atom1Feed
import xml.etree.ElementTree as ET

import models
from videobin.session.models import getUserSettings, UserSettings

def index(request):
    bins = models.Bin.objects.filter(user_key=request.session.session_key).order_by("-updated")[:5]
    context = RequestContext(request, {'bins': bins})
    return render_to_response('index.html', context)

def bins(request):
    bins = models.Bin.objects.filter(user_key=request.session.session_key)
    settings = getUserSettings(request.session.session_key)
    many_emails = False
    if settings.email_address:
        many_emails = UserSettings.objects.filter(email_address=settings.email_address).count() > 1
    context = RequestContext(request, {'bins': bins, 'settings': settings, 'many_emails': many_emails})
    return render_to_response('bins.html', context)

def bin(request, binId):
    bin = get_object_or_404(models.Bin, pk=int(binId, 36))
    if bin.videos.count() > 0:
        video = bin.videos.all()[0]
        return HttpResponseRedirect(video.get_absolute_url())
    context = RequestContext(request, {'bin': bin})
    return render_to_response('bin.html', context)

def opml(request, binId):
    bin = get_object_or_404(models.Bin, pk=int(binId, 36))
    opml = ET.Element('opml')
    opml.attrib['version'] = '2.0'
    head = ET.SubElement(opml, "head")
    title = ET.SubElement(head, "title")
    title.text = bin.title
    dateCreated = ET.SubElement(head, "dateCreated")
    dateCreated.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    docs = ET.SubElement(head, "docs")
    docs.text = "http://www.opml.org/spec2"
    body = ET.SubElement(opml, "body")
    outline = ET.SubElement(body, "outline")
    outline.attrib['xmlUrl'] = bin.atomLink()
    outline.attrib['type'] = 'atom'
    outline.attrib['text'] = bin.title
    f = u'''<?xml version="1.0" encoding="utf-8"?>\n''' + ET.tostring(opml)
    return HttpResponse(f, content_type="application/rss+xml")

def atom_entry(video):
    entry = ET.Element("entry")
    title = ET.SubElement(entry, "title")
    title.text = video.title
    link = ET.SubElement(entry, "link")
    link.attrib['rel'] = 'alternate'
    link.attrib['href'] = video.get_absolute_url()
    updated = ET.SubElement(entry, "updated")
    updated.text = video.updated.strftime("%Y-%m-%dT%H:%M:%SZ")
    published = ET.SubElement(entry, "published")
    published.text = video.created.strftime("%Y-%m-%dT%H:%M:%SZ")
    el = ET.SubElement(entry, "id")
    el.text = video.get_absolute_url()
    '''
    el = ET.SubElement(entry, "media:thumbnail")
    el.attrib['url'] = absolute_url(self.stillLink)
    '''
    el = ET.SubElement(entry, "author")
    name = ET.SubElement(el, "name")
    name.text = video.bin.title
    '''
    el = ET.SubElement(entry, "rights")
    el.text = 'No Copyright'
    el = ET.SubElement(entry, "contributor")
    name = ET.SubElement(el, "name")
    name.text = "Some Name"
    el = ET.SubElement(entry, "category")
    el.attrib['term'] = 'Tag'
    el = ET.SubElement(entry, "category")
    el.attrib['term'] = 'Tag'
    el.attrib['scheme'] = "http://transmission.cc/Genres"
    '''

    content = ET.SubElement(entry, "content")
    content.attrib['type'] = 'text'
    if video.description != 'Add Description':
      content.text = video.description
    else:
      content.text = ' '

    """
    content_format = ET.SubElement(entry, "format")
    content_format.attrib['xmlns'] = 'http://transmission.cc/FileFormat'
    video.format(content_format)
    """

    #BitTorrent Link
    el = ET.SubElement(entry, "link")
    el.attrib['rel'] = 'enclosure'
    el.attrib['type'] = 'application/x-bittorrent'
    el.attrib['href'] = video.torrentLink()
    #FIXME: to be strickt, this should be size of torrent
    el.attrib['length'] = unicode(video.size)

    #HTTP Link
    '''
    el = ET.SubElement(entry, "link")
    el.attrib['rel'] = 'enclosure'
    el.attrib['type'] = 'application/ogg'
    el.attrib['href'] = self.videoLink
    el.attrib['length'] = unicode(self.size)
    '''

    '''
    #Subtitle Link
    el = ET.SubElement(entry, "link")
    el.attrib['rel'] = 'subtitle'
    el.attrib['type'] = 'text/x-srt'
    el.attrib['href'] = self.subtitleLink
    el.attrib['hreflang'] = 'en'
    el.attrib['length'] = self.subtitleSize
    '''
    return entry

def atom(request, binId):
    bin = get_object_or_404(models.Bin, id=int(binId, 36))
    feed = ET.Element("feed")
    feed.attrib['xmlns'] = 'http://www.w3.org/2005/Atom'
    feed.attrib['xmlns:media'] = 'http://search.yahoo.com/mrss'
    feed.attrib['xml:lang'] = 'en'
    title = ET.SubElement(feed, "title")
    title.text = bin.title
    title.attrib['type'] = 'text'
    link = ET.SubElement(feed, "link")
    link.attrib['rel'] = 'self'
    link.attrib['type'] = 'application/atom+xml'
    link.attrib['href'] = bin.atomLink()
    rights = ET.SubElement(feed, 'rights')
    rights.attrib['type'] = 'text'
    rights.text = "No Copyright"
    el = ET.SubElement(feed, 'id')
    el.text = bin.atomLink()
    updated = ET.SubElement(feed, "updated")
    updated.text = bin.updated.strftime("%Y-%m-%dT%H:%M:%SZ")

    for video in bin.videos.all():
      if not video.encoding:
        feed.append(atom_entry(video))

    f =  u'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(feed)
    return HttpResponse(f, content_type="application/rss+xml")

