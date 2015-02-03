# Adding SwampDragon to an existing Django project

Update settings.py to include ```swampdragon``` to installed apps

    INSTALLED_APPS = (
        ...
        'swampdragon',
    )


Add

    # SwampDragon settings
    SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')

to the settings file.

Download [server.py](https://raw.githubusercontent.com/jonashagstedt/swampdragon/master/swampdragon/app_templates/server.py) 
and replace ```<project>``` with your project name (look in manage.py if unsure).

