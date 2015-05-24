# Publishing data

Sometimes you might want to publish data outside of a router, like a celery job or similar.
This can be achived by using ```publish_data```.

## example

A celery task could look something like this:
    
    from swampdragon.pubsub_providers.data_publisher import publish_data
    
    @task()
    def my_task():
        data = get_some_data()  # get_some_data would return a dictionary
        publish_data(channel='foo', data=data)
