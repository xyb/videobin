# -*- coding: utf-8 -*-
# -*- Mode: Python; -*-
# vi:si:et:sw=2:sts=2:ts=2
#
import os
import time
import signal

from BitTornado import bitfield
from BitTornado import piecebuffer
from BitTornado.launchmanycore import LaunchMany
from BitTornado.ConfigDir import ConfigDir
from BitTornado.parseargs import parseargs
from BitTornado.download_bt1 import defaults
from BitTornado.bencode import bencode, bdecode
from BitTornado.BT1.btformats import check_info

from os.path import exists, isfile, basename
import sha
import sys
import thread

import models

DEBUG=0

def formatRate(rate):
  kbit = rate / 1024
  if kbit > 1024:
    mbit = kbit / 1024
    return "%0.2f Mb/s" % mbit
  return "%0.2f Kb/s" % kbit

class TorrentDisplay:
  def __init__(self, ui = None):
    self.ui = ui

  def display(self, data):
    for torrent in data:
      (name, status, progress, peers, seeds, seedsmsg, dist,
          uprate, dnrate, upamt, dnamt, size, t, msg ) = torrent
      percent = "%0.1f%%" %(100* float(upamt)/size)
      _status = "%s uploaded (%s)" % (percent, formatRate(uprate))
      if status == 'checking existing data':
        _status = "checking %s" % progress
      elif seeds == 1 or float(upamt)/size >= 1.0:
        _status = "done"
        if uprate:
          _status += ", still uploading with %s" % formatRate(uprate)
      elif status == 'seeding':
        _status = "seeding, connecting to peers"
      elif peers == 0 and seeds == 0:
        _status = "connecting to peers"
      if self.ui:
        self.ui.updateItemStatus(name, _status)
      else:
        print name
        print _status, dist, "%0.2f" %(100* float(upamt)/size)
        print "\t", 'peers', peers, 'seed', seeds

  def message(self, s):
    if DEBUG:
      print "message", s

  def exception(self, s):
    if DEBUG:
      print "exception", s

class TorrentClient(LaunchMany):
  done = False
  torrent_cache = []
  def __init__(self, config, Output, ui = None):
    if ui:
      ui.torrentClient = self
    LaunchMany.__init__(self, config, Output)
    self.done = True

  def scan(self):
    return

  def join(self):
    self.doneflag.set()
    while not self.done:
      time.sleep(2)
    return

  def removeByName(self, name):
    for t in self.torrent_cache:
      if self.torrent_cache[t]['name'] == name:
        del self.torrent_cache[t]
        self.remove(t)

  def addFile(self, p):
    ff = open(p, 'rb')
    data = ff.read()
    ff.close()
    return self.addTorrent(data, p)

  def addTorrent(self, data, p):
    d = bdecode(data)
    check_info(d['info'])
    h = sha.sha(bencode(d['info'])).digest()
    a = {}
    a['path'] = p
    f = basename(p)
    a['file'] = f
    a['type'] = True
    i = d['info']
    l = 0
    nf = 0
    if i.has_key('length'):
        l = i.get('length',0)
        nf = 1
    elif i.has_key('files'):
        for li in i['files']:
            nf += 1
            if li.has_key('length'):
                l += li['length']
    a['numfiles'] = nf
    a['length'] = l
    a['name'] = i.get('name', f)
    def setkey(k, d = d, a = a):
        if d.has_key(k):
            a[k] = d[k]
    setkey('failure reason')
    setkey('warning message')
    setkey('announce-list')
    a['metainfo'] = d
    if not self.torrent_cache.has_key(h):
      self.torrent_cache[h] = a
      self.add(h, a)
    return self.torrent_cache[h]['name']

def torrentClient(ui = None):
  defaults.extend( [
        ( 'parse_dir_interval', 30,
          "how often to rescan the torrent directory, in seconds" ),
        ( 'crypto_allowed', 0,
          "how often to rescan the torrent directory, in seconds" ),
        ( 'saveas_style', 2,
          "How to name torrent downloads (1 = rename to torrent name, " +
          "2 = save under name in torrent, 3 = save in directory under torrent name)" ),
        ( 'display_path', False, ''),
    ] )
  configdir = ConfigDir('rfbackend')
  defaultsToIgnore = ['responsefile', 'url', 'priority']
  configdir.setDefaults(defaults,defaultsToIgnore)
  configdefaults = configdir.loadConfig()

  defaults.append(('save_options',0,
   "whether to save the current options as the new default configuration " +
   "(only for btlaunchmany.py)"))
  config, args = parseargs(['/tmp'], defaults, 1, 1, configdefaults)
  configdir.deleteOldCacheData(config['expire_cache_data'])
  config['torrent_dir'] = ''

  #launch client and return it
  display = TorrentDisplay(ui)
  torrentThread = thread.start_new_thread(TorrentClient,(config, display, ui))
  time.sleep(2)
  return torrentThread

class BtUi:
  torrentClient = None

  def updateItemStatus(self, name, _status):
    if DEBUG:
      print name, _status
    return

def runClient():
  ui = BtUi()

  def TERMhandler(signum, frame):
    ui.torrentClient.join()
    sys.exit()
  signal.signal(signal.SIGTERM, TERMhandler)

  try:
    torrentClient(ui)
    models.Video.objects.all().update(seeding=False)
    while True:
      for v in models.Video.objects.filter(seeding=False,encoding=False,encoding_failed=False):
        if DEBUG:
          print "add", v.torrent.path
        if v.torrent and os.path.exists(v.torrent.path):
          name = ui.torrentClient.addFile(v.torrent.path)
          #also remove if needed
          #ui.torrentClient.removeByName(name)
          v.seeding = True
          v.save()
      #remove files that are no longer available
      keys = ui.torrentClient.torrent_cache.keys()
      for key in keys:
        p = ui.torrentClient.torrent_cache[key]['path']
        if not os.path.exists(p):
          if DEBUG:
            print "removing", p
          ui.torrentClient.remove(key)
          del ui.torrentClient.torrent_cache[key]
      if DEBUG:
        print "SLEEP: 120"
      time.sleep(120)
  except KeyboardInterrupt:
      print "shutting down..."
      # ^C to exit..
      pass
  ui.torrentClient.join()
