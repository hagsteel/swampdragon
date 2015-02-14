/***********************
 * Swamp Dragon setup
 ***********************/
swampdragon.ready(function () {
    subscribe();
});


function subscribe () {
    swampdragon.subscribe('chat-route', 'local-channel', null, function (context, data) {
        // any thing that happens after successfully subscribing
    }, function (context, data) {
        // any thing that happens if subscribing failed
    });
}


swampdragon.onChannelMessage(function (chanel, data) {
    addMessage(data.name, data.message);
});


/***********************
 * Wire up DOM events
 ***********************/
document.getElementById("send-message-button").addEventListener("click", function () {
    var name = document.getElementById("name").value;
    var message = document.getElementById("message").value;
    sendMessage(name, message);
});


function addMessage (name, msg) {
    var messages = document.getElementById("messages");

    var div = document.createElement("div");
    messages.insertBefore(div, messages.firstChild);
    div.innerHTML = "<span class='label label-primary'>" + name + "</span> " + msg;
}


function sendMessage (name, message) {
    // Reset error messages
    document.getElementById('error-name').innerHTML = "";
    document.getElementById('error-message').innerHTML = "";

    // Send message
    swampdragon.callRouter('chat', 'chat-route', {name:name, message:message}, null, function (e, error) {
        for (var propname in error) {
            document.getElementById('error-' + propname).innerHTML = error[propname];
        }
    });
}