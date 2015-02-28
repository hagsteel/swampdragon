var callbackQueue = {};
callbackId = 0;

function getCallbackName() {
    var callbackName = 'cb_' + callbackId;
    callbackId += 1;
    if (callbackId > 999999) callbackId = 0;
    return callbackName;
}


function on(event, callback) {
    callbackQueue[event] = callbackQueue[event] || [];
    callbackQueue[event].push(callback);
}


function emit(event, args) {
    var queue = callbackQueue[event],
        i = 0, fn;
    if (queue === undefined) {
        return 0;
    }
    for (i = 0; i < queue.length; i += 1) {
        fn = queue[i];
        fn.apply(this, args);
    }
    return queue.length;
}


function emitOnce(event, args) {
    var eventCount = emit(event, args);
    delete callbackQueue[event];
}


module.exports = {
    on: on,
    emit: emit,
    emitOnce: emitOnce,
    getCallbackName: getCallbackName
};
