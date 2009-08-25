var osx = false;
dtv = false;

function dtvapiInitialize(cookie) {
}

function dtvapiAddChannel(url) {
  if(navigator.platform.indexOf('mac')>=0) {
    osx = true;
  }
  if(dtv) {
    document.location.href = ('action:addFeed?selected=0&url='+escape(url));
  }
  else if(osx){
    document.location.href = ('miro:'+url);
  }
  else {
    document.location.href = (url);
  }
  return false;
}

function dtvapiGoToChannel(url) {
  document.location.href = ('action:addFeed?selected=1&url='+escape(url));
  return false;
}
