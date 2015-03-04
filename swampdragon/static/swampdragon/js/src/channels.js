var _channels = {},
    CHANNEL_DATA_SUBSCRIBE = 'subscribe',
    CHANNEL_DATA_UNSUBSCRIBE = 'unsubscribe';


function addRemoteChannel(remote, local) {
    var i;

    if (remote in _channels) {
        for (i = 0; i < _channels[remote].length; i += 1) {
            if (_channels[remote][i] === local) {
                return
            }
        }
        _channels[remote].push(local)
    } else {
        _channels[remote] = [local];
    }
}


function removeRemoteChannel(remote, local) {
    delete _channels[remote];
}


function getLocalChannels(remote) {
    return _channels[remote];
}


function setupChannels(channelSetup) {
    var remoteChannels = channelSetup.remote_channels,
        remoteChannelCount = channelSetup.remote_channels.length,
        i;

    for (i = 0; i < remoteChannelCount; i += 1) {
        if (channelSetup.action === CHANNEL_DATA_SUBSCRIBE) {
            addRemoteChannel(remoteChannels[i], channelSetup.local_channel);
        }
        if (channelSetup.action === CHANNEL_DATA_UNSUBSCRIBE) {
            removeRemoteChannel(remoteChannels[i], channelSetup.local_channel);
        }
    }
}


module.exports = {
    setupChannels: setupChannels,
    getLocalChannels: getLocalChannels
};
