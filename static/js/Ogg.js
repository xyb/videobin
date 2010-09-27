/*
 * Ogg.js Version 1.0.1
 *
 *  <video> element fallback support with help of plugins (totem, xiphQT, cortado)
 *
 * GPL 2007 <j@v2v.cc>
 * 
 * Usage:
 *  <script type="text/javascript">
 *    var OggCortadoLocation = 'http://example.com/cortado.jar';
 *  </script>
 *  <script type="text/javascript" src="Ogg.js">
 *  </script>
 *  <video src="http://example.com/sample.ogg" id="exampleVideo" 
 *                                 width="320" height="240" autoplay="true" />
 *  
 * Parameters are:
 *  - src url/path to ogg file
 *  - width
 *  - height
 *  - autoplay(optional) [start movie right away, default true, values: true|false]
 *  - length(optional) [makes seeking possible in cortado]
 *
 * to set cortado location set OggCortadoLocation before including Ogg.js
 */
if (typeof Ogg == "undefined") {
  var Ogg = new Object();
}

/*
 * check if we are running internet explorer
 */
Ogg.webkit = ( navigator.vendor && navigator.userAgent.search(/WebKit/) > 0);

Ogg.ie = function() {
  if(this.webkit)
    return false;
  return !(navigator.plugins && navigator.plugins.length);
};

/*
 * check for Windows
 */
Ogg.windows = function() {
  return (navigator.platform.indexOf('Win') != -1)
};


/*
 * VideoElement, return dom object of supported plugin,
 *
 */
Ogg.VideoElement = function(url, id, width, height, autoplay, seconds) {
  if (typeof autoplay == "undefined")
    autoplay = "false";
  if (typeof seconds == "undefined")
    seconds = -1;
  if (!seconds)
    seconds = -1;
  if(this.ie()) {
    element = document.createElement('div');
    element.innerHTML = '' +
    '<object classid="clsid:8AD9C840-044E-11D1-B3E9-00805F499D93" '+
    '  codebase="http://java.sun.com/update/1.5.0/jinstall-1_5_0-windows-i586.cab" '+
    '  id="' + id + '" '+
    '  width="' + width + '" height="' + height + '">'+
    ' <param name="code" value="com.fluendo.player.Cortado" />'+
    ' <param name="archive" value="' + this.CortadoLocation + '" />'+
    ' <param name="duration" value="' + video_duration + '" />'+
    ' <param name="url" value="' + url + '" /> '+
    ' <param name="local" value="false" /> '+
    ' <param name="keepAspect" value="false" /> '+
    ' <param name="video" value="true" /> '+
    ' <param name="audio" value="true" /> '+
    ' <param name="seekable" value="auto" /> '+
    ' <param name="showStatus" value="auto" /> '+
    ' <param name="bufferSize" value="200" /> '+
    ' <param name="autoPlay" value="' + autoplay + '" /> '+
    ' <strong>Your browser does not support HTML5 Video. Get a modern browser like <a href="http://www.mozilla.com/firefox">Firefox 3.5</a>.</strong>' +
    '</object>';
    f = document.createTextNode('');
    element.appendChild(f);
    element = element.firstChild;
    
    //add native <video> js callbacks
    //disabled since it breaks IE, patch welcome
    /*
    element.play = function() {
      this.doPlay();
      this.isPlaying = true;
    }
    element.pause = function() {
      this.doPause();
      this.isPlaying = false;
    }
    element.stop = function() {
      this.doStop();
      this.isPlaying = false;
    }
    */
  } else if (detectTotem()) {
    element = document.createElement('embed');
    element.type = 'application/ogg';
    element.id = id;
    element.width = width;
    element.height = height;
    element.setAttribute('src', url);
    element.setAttribute('controller', false);
    element.setAttribute('autoplay', 'true');
  } else if (detectMimetype('application/x-vlc-plugin')) {
    element = document.createElement('embed');
    element.type = 'application/x-vlc-plugin';
    element.setAttribute('target', url);
    element.id = id;
    element.width = width;
    element.height = height;
    element.setAttribute('autoplay', 'yes');
    //controler: false
  } else if (detectMimetype('2application/ogg')) {
    element = document.createElement('object');
    if(this.windows()) { //VLC plugin in Firefox needs extra treatment
      element.type = 'application/ogg';
      element.data = url;
    }
    else {
      element.type = 'video/quicktime';
      //element.data = '/static/video.mov';
      element.data = url;
    }
    element.id = id;
    element.width = width;
    element.height = height;
    
    params = {
      'qtsrc': url,
      'AutoPlay': autoplay,
      'SCALE': 'Aspect',
      'controller': 'false'
    }
    for(name in params){
      var p = document.createElement('param');
      p.name = name;
      p.value = params[name];
      element.appendChild(p);
    }
    // this is only needed for the QuickTime Component
    element.play = function() {
      this.Play();
      this.isPlaying = true;
    }
    element.pause = function() {
      this.Pause();
      this.isPlaying = false;
    }
    element.stop = function() {
      this.Stop();
      this.isPlaying = false;
    }
  } else if(detectMimetype('application/x-java-applet') || navigator.javaEnabled()) {
    element = document.createElement('object');
    element.setAttribute('classid', 'java:com.fluendo.player.Cortado.class');
    element.type = 'application/x-java-applet';
    element.setAttribute('archive', this.CortadoLocation);
    element.id = id;
    element.width = width;
    element.height = height;
    
    var params = {
      'code': 'com.fluendo.player.Cortado',
      'archive': this.CortadoLocation,
      'url': url,
      'local': 'false',
      'keepAspect': 'true',
      'video': 'true',
      'audio': 'true',
      'seekable': 'auto',
      'showStatus': 'auto',
      'autoPlay': autoplay,
      'duration': video_duration,
      'bufferSize': '500'
    }
    for(name in params){
      var p = document.createElement('param');
      p.name = name;
      p.value = params[name];
      element.appendChild(p);
    }
    
    //add native <video> js callbacks
    element.play = function() { 
      this.doPlay();
    }
    element.pause = function() {
      this.doPause();
    }
    element.stop = function() {
      this.doStop();
    }
  }
  else {
    //FIXME: should give better advice based on browser and os
    element = document.createElement('div');
    element.id = id;
    element.style.width = width;
    element.style.height = height;
    element.style.background = '#ddd';
    notice = document.createTextNode('');
    element.innerHTML = '<div style="height:100%;padding:10%;padding-top:30%;">Your browser does not support HTML5 Video. Get a modern browser like <a href="http://www.mozilla.com/firefox">Firefox 3.5</a>.</div>';
    element.appendChild(notice);
  }
  return element;
};


Ogg.init = function() {
  if(typeof(OggCortadoLocation) == 'undefined')
    this.CortadoLocation = '/static/cortado.g4bdec5b.jar';
  else
    this.CortadoLocation = OggCortadoLocation;

  var v = document.createElement('video');
  if (v) {
      this.theora = !!(v.canPlayType && v.canPlayType('video/ogg; codecs="theora, vorbis"').replace(/no/, ''));
  } else {
      this.theora = false;
  }
  if(this.theora)
    return;
  var VideoElements = document.getElementsByTagName("video");
  for(i = 0; i < VideoElements.length; i++) {
    var v = VideoElements[i];
    var video = this.VideoElement(
        v.getAttribute('src'), 
        v.getAttribute('id'),
        v.getAttribute('width'),
        v.getAttribute('height'),
        v.hasAttribute('autoplay'),
        v.getAttribute('length')
    );
    var p = v.parentNode;
    p.removeChild(v);
    p.appendChild(video);
    i--;
  }
};

Ogg.cortadoToggle = function(el) {
  if(typeof(el.isPlaying) == 'undefined') {
    el.isPlaying = true;
  }
  if(el.isPlaying) {
    el.isPlaying = false;
    el.doPause();
  }
  else {
    el.isPlaying = true;
    el.doPlay();
  }
};

Ogg.Toggle = function(el) {
  if(typeof(el.isPlaying) == 'undefined') {
    el.isPlaying = true;
  }
  if(el.isPlaying) {
    el.isPlaying = false;
    el.pause();
  }
  else {
    el.isPlaying = true;
    el.play();
  }
};

function detectVLC() {
  var mimetype="application/x-vlc-plugin";
  var vlc = false;
  var totem = false;
  for (var i = navigator.plugins.length; i-- > 0; ) {
    var plugin = navigator.plugins[i];
    if (typeof plugin[mimetype] != "undefined") {
      if(plugin.name.toLowerCase().match('totem')) {
        totem = true;
      } else {
       vlc = true;
      }
    }
  }
  if(totem) vlc=false;
  return vlc;
}

function detectMimetype(mimetype) {
  for (var i = navigator.plugins.length; i-- > 0; ) {
    var plugin = navigator.plugins[i];
    if (typeof plugin[mimetype] != "undefined") {
      return true;
    }
  }
  return false;
};

function detectTotem() {
  var mimetype="application/ogg";
  for (var i = navigator.plugins.length; i-- > 0; ) {
    var plugin = navigator.plugins[i];
    if (typeof plugin[mimetype] != "undefined") {
      if(plugin.name.toLowerCase().match('totem')) {
        return true;
      }
    }
  }
  return false;
}


function oggAddEvent(obj, evType, fn){ 
 if (obj.addEventListener){ 
   obj.addEventListener(evType, fn, false); 
   return true; 
 } else if (obj.attachEvent){ 
   var r = obj.attachEvent("on"+evType, fn); 
   return r; 
 } else { 
   return false; 
 } 
}
oggAddEvent(window, 'load', function() { Ogg.init() });
