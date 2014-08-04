// Originated from http://jsfiddle.net/danielzen/utp7j/
var uploadFile = function (element, dest, uploadComplete) {
    var that = this;
    var url = window.swampDragon.url + '/_sdfileupload/';
    var fd = new FormData();
    for (var i in element.files) {
        fd.append("uploadedFile", element.files[i]);
    }
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress", uploadProgress, false);
    xhr.addEventListener("load", uploadComplete, false);
    xhr.addEventListener("error", uploadFailed, false);
    xhr.addEventListener("abort", uploadCanceled, false);
    xhr.open("POST", url, true);
    xhr.send(fd);
};

//function uploadCompleteOrig(evt) {
//    /* This event is raised when the server send back a response */
//    console.log(evt.target.responseText)
//}

function uploadFailed(evt) {
    console.log("There was an error attempting to upload the file.")
}

function uploadCanceled(evt) {
//    scope.$apply(function () {
//        scope.progressVisible = false
//    });
    console.log("The upload has been canceled by the user or the browser dropped the connection.")
}

function uploadProgress(evt) {
//    console.log(evt);
//    scope.$apply(function () {
//        if (evt.lengthComputable) {
//            scope.progress = Math.round(evt.loaded * 100 / evt.total);
//        } else {
//            scope.progress = 'unable to compute';
//        }
//    })
}
