# Calling routers

## Disconnect

    window.swampDragon.disconnect();
    
This will disconnect the client from the server.
    

## CallRouter

```callRouter``` issues a call to a specific router

    window.swampDragon.callRouter(verb, route, args, callbackName)
    
*  ```verb``` is the verb on the router. The verb needs to exist in ```valid_verbs``` on the router.
*  ```route``` is the name of the router (this is defined on the router as ```route_name```).
*  ```args``` is the data to be sent.
*  ```callbackName``` is required if the router needs to respond to the call.

The following example shows calling a router. 

    window.swampDragon.on('receivedNews', function(context, data) {
        this.news = data;
    });
    window.swampDragon.callRouter('news', 'get_list', {topic: 'python'}, 'receivedNews');


## get_single

```get_single``` call a (model) router for a single instance of an object.

    window.swampDragon.on('gotNewsItem', function(context, data) { ... });
    window.swampDragon.get_single('news', {id: 1}, 'gotNewsItem');
    

## get_list 

```get_list``` calls a router to get a list of objects.

    window.swampDragon.on('receivedNews', function(context, data) { ... });
    window.swampDragon.get_list('news', {topic: 'python'}, 'receivedNews');


## create_object

```create_object``` calls a router and ask it to create an object.

    window.swampDragon.on('newsCreated', function(context, data) {
        if (context.state == 'success') {
            console.log('created news ' + data.title);
        }
        
        if (context.state == 'error') {
            console.log('failed to create news: ' + data);
        }
    });
    
    window.swampDragon.create_object('news', {
        topic: 'python', 
        title: 'Hssss', 
        content: 'snakes or code'
    }, 'newsCreated');


## update_object

```update_object``` calls a router with data and ask it to update an object.

    window.swampDragon.update_object('news', {
        topic: 'python', 
        title: 'Python 3', 
        content: 'A story about python 3',
        id: 32
    }, 'newsUpdated');


## delete_object

```delete_object``` calls a router with data and ask it to delete an object.

    window.swampDragon.on('newsDeleted', function(context, data) {
        this.news.findAndDelete(data.id);
    });
    window.swampDragon.delete_object('news', {id: 32}, 'newsDeleted');


## subscribe

```subscribe``` to a channel.

    window.swampDragon.subscribe('movies', {
        genre: ['comedy', 'action']
    }, 'subscribeCallback', 'mymovies');


## unsubscribe

```unsubscribe``` from a channel.

    window.swampDragon.unsubscribe('movies', 'unsubscribeCallback', 'mymovies');
