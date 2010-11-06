# Create your views here.
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.conf import settings as videobin_settings
from django.core.mail import send_mail

from videobin.bin.models import Bin
from videobin.utils.shortcuts import render_to_json_response

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader, Context

import models


def recover(request, key):
    #only update if the key is not already active
    if request.session.session_key != key:
        #take over email from old key
        newSettings = models.getUserSettings(request.session.session_key)
        if not newSettings.email_address:
            oldSettings = models.getUserSettings(key)
            newSettings.email_address = oldSettings.email_address
            newSettings.save()
            oldSettings.delete()
        #transfer ownership to new session key
        Bin.objects.filter(user_key=key).update(user_key=request.session.session_key)
        #remove old session
        Session.objects.filter(session_key=key).delete()
        #merge old sessions
        settings = models.getUserSettings(request.session.session_key)
        if settings.email_address:
            for s in models.UserSettings.filter(email_address=settings.email_address):
                if s.user_key != request.session.session_key:
                    Bin.objects.filter(user_key=s.user_key).update(user_key=request.session.session_key)
                s.delete()

    return HttpResponseRedirect('/bins')

def recover_request(request):
    email = request.POST.get('email', None)
    if email:
        q = models.UserSettings.objects.filter(email_address = email)
        if q.count() > 0:
            key = q[0].user_key
            if key == request.session.session_key:
                return HttpResponseRedirect('/bins')
            #send recovery mail
            template = loader.get_template('recover_mail.txt')
            context = Context({
                'recover_url': request.build_absolute_uri("/r/%s" % key),
            })
            subject =  'VideoBin Account Recovery'
            message = template.render(context)
            send_mail(subject, message, videobin_settings.CONTACT_EMAIL, [email, ])
            return HttpResponseRedirect('/recover')
    return HttpResponseRedirect('/')

def recover_sent(request):
    context = RequestContext(request, {})
    return render_to_response('recover.html', context)

def settings(request):
    response = dict(result=False)
    email_address = request.GET.get('email_address', None)
    if email_address:
        settings = models.getUserSettings(request.session.session_key)
        settings.email_address = email_address
        settings.save()
        response = dict(result=True)
    return render_to_json_response(response)

