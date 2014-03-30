def format_message(data, context, channel_setup=None):
    message = dict({'data': data})
    message['context'] = context
    if channel_setup:
        message['channel_data'] = channel_setup
    return message
