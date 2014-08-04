// Originated from http://jsfiddle.net/danielzen/utp7j/
var uploadFile = function (files, uploadComplete, uploadProgress) {
    var that = this;
    var url = window.swampDragon.url + '/_sdfileupload/';
    var fd = new FormData();
    for (var i in files) {
        fd.append("uploadedFile", files[i]);
    }
    var xhr = new XMLHttpRequest();
    if (uploadProgress) {
        xhr.upload.addEventListener("progress", uploadProgress, false);
    }
    xhr.addEventListener("load", uploadComplete, false);
    xhr.addEventListener("error", uploadFailed, false);
    xhr.addEventListener("abort", uploadCanceled, false);
    xhr.open("POST", url, true);
    xhr.send(fd);
};

function uploadFailed(evt) {
    console.log("There was an error attempting to upload the file.")
}

function uploadCanceled(evt) {
    console.log("The upload has been canceled by the user or the browser dropped the connection.")
}
