# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

import os
from os.path import basename, splitext, dirname, exists, join

from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.utils import simplejson
from ox import strip_tags
from django.db.models import F
from ox.django.http import HttpFileResponse

import models

from videobin.utils.shortcuts import render_to_json_response 
from videobin.session.models import update_or_create_user


def get_video_or_404(binId, videoId):
    bin = get_object_or_404(models.Bin, pk=int(binId, 36))
    video = get_object_or_404(models.Video, pk=int(videoId, 36))
    if video.bin == bin:
        return video
    raise Http404

def view(request, binId, videoId):
    video = get_video_or_404(binId, videoId)
    ownsBin = (request.session.session_key == video.bin.user_key)
    canAddVideo = (video.bin.writeable or ownsBin)
    shareRawTorrent = settings.SHARE_RAW_TORRENT and video.raw_torrent
    context = RequestContext(request, {
        'autoplay': request.GET.get('autoplay', '1') == '1',
        'video': video,
        'ownsBin': ownsBin,
        'canAddVideo': canAddVideo,
        'shareRawTorrent': shareRawTorrent
    })
    return render_to_response('video.html', context)

def iframe(request, binId, videoId):
    video = get_video_or_404(binId, videoId)
    
    context = RequestContext(request, {
        'autoplay': request.GET.get('autoplay', '0') == '1',
        'video': video,
    })
    if not video.encoding and not video.disabled:
        models.Video.objects.filter(pk=int(videoId, 36)).update(viewed=F('viewed')+1)
    response = render_to_response('iframe.html', context)
    response['Cache-Control'] = 'no-cache'
    return response

def video(request, binId, videoId):
    video = get_video_or_404(binId, videoId)
    if not video.encoding and not video.disabled:
        return HttpFileResponse(video.file.path)
    else:
        raise Http404

def torrent(request, binId, videoId):
    video = get_video_or_404(binId, videoId)
    response = HttpResponse(video.torrent, mimetype="application/x-bittorrent")
    response['Content-Type'] = "application/x-bittorrent"
    torrentName = video.downloadFilename().encode('utf-8') + '.torrent'
    response['Content-Disposition'] = 'attachement; filename="%s"' % torrentName
    return response

def raw_torrent(request, binId, videoId):
    if settings.SHARE_RAW_TORRENT:
        video = get_video_or_404(binId, videoId)
        response = HttpResponse(video.raw_torrent, mimetype="application/x-bittorrent")
        response['Content-Type'] = "application/x-bittorrent"
        torrentName = video.downloadFilename().encode('utf-8') + '.raw.torrent'
        response['Content-Disposition'] = 'attachement; filename="%s"' % torrentName
        return response
    else:
        raise Http404

def edit(request, binId, videoId):
    video = get_video_or_404(binId, videoId)
    ownsBin = (request.session.session_key == video.bin.user_key)
    canEditVideo = (video.bin.writeable or ownsBin)

    def render_to_text_response(response):
        return HttpResponse(response, content_type="text/plain")

    if not canEditVideo:
      response = 'you are not allowd to edit this field'
      return render_to_text_response(response)
    response = 'invalid input'
    if 'title' in request.POST:
      video.title = strip_tags(request.POST['title'])
      video.save()
      response = video.title
    elif 'description' in request.POST:
      #should do better than that, allow some html here
      video.description = strip_tags(request.POST['description'])
      video.save()
      response = video.description.replace('\n', '<br />')
    elif 'binTitle' in request.POST:
      video.bin.title = strip_tags(request.POST['binTitle'])
      video.save()
      response = video.bin.title
    elif 'writeable' in request.GET:
      video.bin.writeable = (request.GET['writeable'] == '1')
      video.bin.save()
      response = dict(writeable=video.bin.writeable)
    return render_to_text_response(response)

def remove(request, binId, videoId):
    user_key = request.session.session_key
    video = get_video_or_404(binId, videoId)
    redirect = video.get_absolute_url()
    if request.method == "POST":
        if user_key == video.bin.user_key:
            bin = video.bin
            video.delete()
            if bin.videos.count() > 0:
                redirect = bin.get_absolute_url()
            else:
                bin.delete()
                redirect = '/'
    return HttpResponseRedirect(redirect)

class VideoChunkForm(forms.Form):
    chunk = forms.FileField()
    done = forms.IntegerField(required=False)

def upload(request, binId, videoId):
    """
    Return json indicating success if chunk upload
    """
    ogg = request.GET.get('ogg', False) == '1'
    raw = request.GET.get('raw', False) == '1'
    if request.method == 'POST':
        video = get_video_or_404(binId, videoId)
        form = VideoChunkForm(request.POST, request.FILES)
        ownsBin = (request.session.session_key == video.bin.user_key)
        canEditVideo = (video.bin.writeable or ownsBin)
        if form.is_valid() and canEditVideo:
            f = form.cleaned_data['chunk']
            response = dict(result=1, resultUrl=request.build_absolute_uri(video.get_absolute_url()))

            if not video.save_chunk(f.read(), raw=raw):
                response['result'] = 'failed'
            elif form.cleaned_data['done']:
                video.done = True
                video.save()
                video.loadMetadata()
                response['result'] = 1
                response['done'] = 1
            return render_to_json_response(response)
    response = dict(result=-1, videoUrl='/')
    return render_to_json_response(response)

def add(request):
    """
    Redirect to video page
    or return json for Firefogg with uploadUrl
    """
    #FIXME: user_visit.id
    user_key = request.session.session_key
    if request.method == 'POST':
        bin = None
        if request.POST.get('bin', None):
          bin = models.Bin.objects.get(pk=int(request.POST['bin'], 36))
        if bin:
            if not bin.writeable and bin.user_key != user_key:
                bin = None
        email = request.POST.get('email', None)
        if email:
            user_key = update_or_create_user(user_key, email)

        firefogg = request.POST.get('firefogg', False)
        chunk = request.POST.get('chunk', False)
        if firefogg or chunk:
            binTitle = '___title___'
            if not bin:
                bin = models.Bin(title=binTitle, description='', user_key=user_key)
                bin.save()
            description = request.POST.get('description', "Add Description")
            title = request.POST.get('title', binTitle)
            video = models.Video(title=title, description=description, bin=bin)
            video.encoding = True
            video.save()
            upload_url = request.build_absolute_uri("%s.chunk" % video.linkBase())
            is_ogg = request.POST.get('name', '').split('.')[-1] in ('ogv', 'ogg') or firefogg
            if chunk and not is_ogg:
                upload_url += '?raw=1'
            else:
                upload_url += '?ogg=1'
            response = dict(result=1, uploadUrl=upload_url)
            return render_to_json_response(response)
        # Save any files that were uploaded (ignoring empty form fields)
        if 'videoFile' in request.FILES:
            videoFile = request.FILES['videoFile']
            binTitle = os.path.splitext(os.path.basename(videoFile.name))[0]
            if not bin:
                bin = models.Bin(title=binTitle, description=videoFile.name, user_key=user_key)
                bin.save()
            description = request.POST.get('description', "Add Description")
            title = request.POST.get('title', binTitle)
            video = models.Video(title=title, description=description, bin=bin)
            video.save()
            if os.path.splitext(videoFile.name)[1] in ('.ogg', '.ogv'):
                video.file.save(videoFile.name, videoFile)
                video.encoding = False
            else:
                video.raw_file.save(videoFile.name, videoFile)
                video.encoding = True
            if not video.encoding:
                video.loadMetadata()
            if title != videoFile.name:
              video.title = title
            video.done = True
            video.save()
            if request.POST.get('api', False):
                return HttpResponse(request.build_absolute_uri(video.get_absolute_url()), content_type="text/plain")
            return HttpResponseRedirect(video.get_absolute_url())

    #no upload
    return HttpResponseRedirect('/')

