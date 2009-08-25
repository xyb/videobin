$(document).ready(function() {
  $('#firefogg').hide();
  if(typeof(Firefogg) != 'undefined') {
    $('#addVideo').hide();
    $('#firefogg').show();
    $('#submitVideo').hide();

    ogg = new Firefogg();
    var passthrough = false;

    $('#selectVideo').click(function() {
      if(ogg.selectVideo()) {
        $('#selectVideo').hide();
        $('#submitVideo').show();
        var contentType = JSON.parse(ogg.sourceInfo).contentType;
        if (contentType == 'video/ogg' || contentType == 'audio/ogg' || contentType == 'application/ogg') {
          passthrough = true;
        }
      }
    });
    $('#submitVideo').click(function() {
      $('#submitVideo').hide();
      $('#progressbar').show();
      $('#progressbar').width(200);
      $('#progressbar').css('background-color', '#eee');
      $('#progressbar').html('<div id="progress" style="background-color: #666;height:20px;" /><div id="progressstatus" style="background-color: #fff;" />')
      var options = JSON.stringify({'maxSize': 512, 'videoBitrate': 700, 'audioQuality': 0, 'noUpscaling': true});
      if (passthrough) {
        options = JSON.stringify({'passthrough': true});
      }
      var data = {}
      var _data = $('#firefogg').serializeArray();
      $(_data).each(function() {
        data[this.name] = this.value;
      })
      data['firefogg'] = 1;
      var data = JSON.stringify(data);
      ogg.upload(options, add_url, data);
      var updateStatus = function() {
        var status = ogg.status();
        var progress = ogg.progress();

        //do something with status and progress, i.e. set progressbar width:
        var progressbar = document.getElementById('progress');
        progressbar.style.width= parseInt(progress*200) +'px';
        $('#progressstatus').html(parseInt(progress*100) + '% - ' + status);

        //loop to get new status if still encoding
        if(ogg.state == 'encoding' || ogg.state == 'uploading') {
          setTimeout(updateStatus, 500);
        }
        //encoding sucessfull, state can also be 'encoding failed'
        else if (ogg.state == 'done') {
          if(ogg.resultUrl)
            document.location.href = ogg.resultUrl;
        } else {
          $('#progressstatus').html(ogg.state);
        }
      }
      updateStatus();
    });
  }
});

