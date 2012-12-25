// vi:si:et:sw=4:sts=4:ts=4
'use strict';

$(function() {
    $('#videoFile').change(function(event) {
        if($('#videoFile')[0].files.length) {
            $('#addVideoSubmit')[0].disabled = false;
        }
    });
    $('#addVideoSubmit').click(function(event) {
        event.preventDefault();
        $('#addVideo').hide();
        $('#progressbar').show();
        $('#progressbar').width(200);
        $('#progressbar').css('background-color', '#eee');
        $('#progressbar').html('<div id="progress" style="background-color: #666;height:20px;" /><div id="progressstatus" style="background-color: #fff;" />');
        updateProgress(0, 'uploading');
        var file = $('#videoFile')[0].files[0],
            data= {
                'chunk': 1,
                'title': file.name.replace(/\.[^.]+$/, ''),
                'name': file.name
            },
            bin = $('#addVideoBin').val();
        if (bin) {
            data.bin = bin;
        }
        ChunkUploader({
          file: file,
          url: add_url,
          data: data,
          progress: function(data) {
            updateProgress(data.progress, 'uploading');
          },
          callback: function(result) {
              var data = JSON.parse(result.responseText);
              if(data.resultUrl) {
                $('#statusBar').html('Upload succeeded.');
                document.location.href = data.resultUrl;
              } else {
                $('#statusBar').html('Upload failed.');
              }
          }
        });
        return false;
    });
});
