// vi:si:et:sw=4:sts=4:ts=4
// GPL2+/MIT 2012
'use strict';
/*
 Usage:
  ChunkUploader({
      file: file,
      url: '/add',
      data: {'name': file.name},
      progress: function(data) {
        console.log(data.progress);
      },
      callback: function(result) {
          if(result.progress == 1) {
              var response = JSON.parse(result.responseText);
              if(response.resultUrl) {
                document.location.href = response.resultUrl;
              } else {
                alert(response.status;
              }
          } else {
              alert('!!!');
          }
      }
  });
*/
function ChunkUploader(options) {
    var chunkSize = options.size || 1024*1024,
        chunkUrl,
        file = options.file,
        maxRetry = -1,
        retries = 0,
        request,
        that = {};

    initUpload();

    function done() {
        options.callback({
          status: that.status,
          progress: that.progress,
          responseText: that.responseText
        });
    }

    function initUpload() {
        //request upload slot from server
        that.status = 'requesting chunk upload';
        that.progress = 0;
        request = new XMLHttpRequest();
        request.addEventListener('load', function (evt) {
            var response = {};
            that.responseText = evt.target.responseText;
            try {
                response = JSON.parse(evt.target.responseText);
            } catch(e) {
                response = {};
                that.status = 'failed to parse response';
                that.progress = -1;
                done();
            }
            if (response.maxRetry) {
                maxRetry = response.maxRetry;
            }
            chunkUrl = response.uploadUrl;
            if (document.location.protocol == 'https:') {
                chunkUrl = chunkUrl.replace(/http:\/\//, 'https://');
            }
            if (chunkUrl) {
                that.status = 'uploading';
                that.progress = 0.0;
                //start upload
                uploadChunk(0);
            } else {
                that.status = 'upload failed, no upload url provided';
                that.progress = -1;
                done();
            }
        }, false);
        request.addEventListener('error', function (evt) {
            that.status = 'uplaod failed';
            that.progress = -1;
            that.responseText = evt.target.responseText;
            done();
        }, false);
        request.addEventListener('abort', function (evt) {
            that.status = 'aborted';
            that.progress = -1;
            done();
        }, false);
        var formData = new FormData();
        
        Object.keys(options.data).forEach(function(key) {
            formData.append(key, options.data[key]);
        });
        request.open('POST', options.url);
        request.send(formData);
    }

    function progress(p) {
        that.progress = p;
        options.progress({
            progress: that.progress,
            status: that.status
        });
    }

    function uploadChunk(chunkId) {
        var bytesAvailable = file.size,
            chunk,
            chunkOffset = chunkId * chunkSize;

        if(file.mozSlice) {
            chunk = file.mozSlice(chunkOffset, chunkOffset+chunkSize, file.type);
        } else if(file.webkitSlice) {
            chunk = file.webkitSlice(chunkOffset, chunkOffset+chunkSize, file.type);
        } else if(file.slice) {
            chunk = file.slice(chunkOffset, chunkOffset+chunkSize, file.type);
        } else {
            that.status = 'Sorry, your browser is currently not supported.';
            done()
        }

        progress(parseFloat(chunkOffset)/bytesAvailable);

        request = new XMLHttpRequest();
        request.addEventListener('load', function (evt) {
            var response;
            that.responseText = evt.target.responseText;
            try {
                response = JSON.parse(evt.target.responseText);
            } catch(e) {
                response = {};
            }
            if (response.done == 1) {
                //upload finished
                that.resultUrl = response.resultUrl;
                that.progress = 1;
                that.status = 'done';
                done();
            } else if (response.result == 1) {
                //reset retry counter
                retries = 0;
                //start uploading next chunk
                uploadChunk(chunkId + 1);
            } else {
                //failed to upload, try again in 5 second
                retries++;
                if (maxRetry > 0 && retries > maxRetry) {
                    that.status = 'uplaod failed';
                    that.progress = -1;
                    done();
                } else {
                    setTimeout(function() {
                        uploadChunk(chunkId);
                    }, 5000);
                }
            }
        }, false);
        request.addEventListener('error', function (evt) {
            //failed to upload, try again in 3 second
            retries++;
            if (maxRetry > 0 && retries > maxRetry) {
                that.status = 'uplaod failed';
                that.progress = -1;
                done();
            } else {
                setTimeout(function() {
                    uploadChunk(chunkId);
                }, 3000);
            }
        }, false);
        request.upload.addEventListener('progress', function (evt) {
            if (evt.lengthComputable) {
                progress(parseFloat(chunkOffset + evt.loaded) / bytesAvailable);
            }
        }, false);
        request.addEventListener('abort', function (evt) {
            that.status = 'aborted';
            that.progress = -1;
            done();
        }, false);

        var formData = new FormData();
        formData.append('chunkId', chunkId);
        if (bytesAvailable <= chunkOffset + chunkSize) {
            formData.append('done', 1);
        }
        formData.append('chunk', chunk);
        request.open('POST', chunkUrl, true);
        request.send(formData);
    }

    that.abort = function() {
        if (request) {
            request.abort();
            request = null;
        }
    };
    return that;
}
