# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core import serializers
from django.utils import feedgenerator
from django.core.mail import send_mail
from django.core.cache import cache

import oxlib

from utils.shortcuts import render_to_json_response


def help(request):
    context = RequestContext(request, {})
    return render_to_response('help.html', context)

def help_encoding(request):
    context = RequestContext(request, {})
    return render_to_response('help_encoding.html', context)

def about(request):
    context = RequestContext(request, {})
    return render_to_response('about.html', context)
 
def code(request):
    context = RequestContext(request, {})
    return render_to_response('code.html', context)

def feedback(request):
    if request.method == 'POST':
        subject =  'VideoBin Feedback'
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        admins = [settings.CONTACT_EMAIL, ]
        if subject and message and from_email:
            #try:
            send_mail(subject, message, from_email, admins)
            #except BadHeaderError:
            #    return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/feedback/thanks')
    context = RequestContext(request, {})
    return render_to_response('feedback.html', context)

def feedback_thanks(request):
    context = RequestContext(request, {})
    return render_to_response('feedback_thanks.html', context)

def upload_progress(request):
    """
    Return json with information about the progress of an upload.
    """
    from django.template import loader, Context
    progress_id = ''
    if 'X-Progress-ID' in request.GET:
        progress_id = request.GET['X-Progress-ID']
    elif 'X-Progress-ID' in request.META:
        progress_id = request.META['X-Progress-ID']
    if progress_id:
        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        d = {}
        if data:
            d['speed'] = oxlib.formatNumber(data['speed'], 'b/s', 'b/s') # kb/s
            d['size'] = oxlib.formatNumber(data['length'], 'B', 'B')
            d['received'] = oxlib.formatBytes(data['uploaded'])
            d['eta'] = oxlib.formatDuration(int(data['eta'] * 1000), milliseconds=False)
            d['precents'] =  "%d" % int(int(data['uploaded'])*100/int(data['length']))

            template = loader.get_template('progressbar.html')
            context = Context(d)
            d['progressbar_html'] = template.render(context)
        return render_to_json_response(d)
    else:
        return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

