$(document).ready(function() {
  function updateProgress(progress, status) {
      $('#progress').css({
        width: Math.round(progress*200) + 'px'
      });
      $('#progressstatus').html(
        Math.round(progress*100) + ' % - ' + status
      );
  }
  $('#firefogg').hide();
  if(typeof(Firefogg) != 'undefined') {
    $('#addVideo').hide();
    $('#firefogg').show();
    $('#submitVideo').hide();

    var ogg = new Firefogg(),
        passthrough = false;

    $('#selectVideo').click(function() {
      if(ogg.selectVideo()) {
        $('#selectVideo').hide();
        $('#submitVideo').show();
        var contentType = JSON.parse(ogg.sourceInfo).contentType;
        if (contentType == 'video/ogg' ||
            contentType == 'audio/ogg' ||
            contentType == 'application/ogg') {
          passthrough = true;
        }
      }
    });
    $('#submitVideo').click(function() {
      $('#submitVideo').hide();
      $('#progressbar').show();
      $('#progressbar').width(200);
      $('#progressbar').css('background-color', '#eee');
      $('#progressbar').html('<div id="progress" style="background-color: #666;height:20px;" /><div id="progressstatus" style="background-color: #fff;" />');
      var options;
      if (passthrough) {
        updateProgress(0, 'uploading');
        options = JSON.stringify({'passthrough': true});
      } else {
        updateProgress(0, 'encoding');
        options = JSON.stringify({
            'maxSize': 512,
            'videoBitrate': 700,
            'audioQuality': 0,
            'noUpscaling': true
        });
      }
      var postData = {
        firefogg: 1
      };
      var _data = $('#firefogg').serializeArray();
      $(_data).each(function() {
        postData[this.name] = this.value;
      });
      postData = JSON.stringify(postData);
      ogg.encode(options,
        function(data) { //encoding done
          data = JSON.parse(data);
          if(data.progress == 1) {
            ogg.chunk_upload(add_url, postData, function(data) {
              //done
              data = JSON.parse(data);
              if(data.resultUrl) {
                $('#statusBar').html('Upload succeeded.');
                document.location.href = data.resultUrl;
              } else {
                $('#statusBar').html('Upload failed.');
              }
            }, function(data) { //upload progress
              data = JSON.parse(data);
              updateProgress(data.progress, 'uploading');
            });
          } else {
              $('#progressstatus').html("Encoding failed.");
          }
        }, function(data) { //encoding progress
          data = JSON.parse(data);
          updateProgress(data.progress, 'encoding');
        });
    });
  }
});

