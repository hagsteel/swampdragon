# Quick start

Install Swamp Dragon: ```pip install swampdragon```, or download the latest source from 
[Github](https://github.com/jonashagstedt/swampdragon). 


To start a new project run 

    dragon-admin startproject <project name>

Create the initial app

    django-admin.py startapp <module name>
    
    
Add a model to your app

    from django.db import models
    from swampdragon.models import SelfPublishModel
    
    
    class Foo(SelfPublishModel, models.Model):
        text = models.CharField(max_length=100)


Create serializers.py in your app directory.

    from swampdragon.serializers.model_serializer import ModelSerializer
    
    
    class FooSerializer(ModelSerializer):
        class Meta:
            model = 'myapp.Foo'
            publish_fields = ('text', )
            update_fields = ('text', )


Add routers.py to your app directory (same as your models.py, and serializers.py)
  
    from swampdragon import route_handler
    from swampdragon.route_handler import BaseModelPublisherRouter
    from .serializers import FooSerializer
    from .models import Foo
    
    
    class FooRouter(BaseModelPublisherRouter):
        serializer_class = FooSerializer
        model = Foo
        route_name = 'foo'
    
        def get_object(self, **kwargs):
            return self.model.objects.get(pk=kwargs['pk'])
    
        def get_query_set(self, **kwargs):
            return self.model.all()
    
    
    route_handler.register(FooRouter)


Update settings.py to include your new app:
 
     INSTALLED_APPS = (
        ...
        'myproject.myapp',
    )


For django to be able to find your templates you need to add at least one template dir.
Append the following to the end of your settings.py file

    
    TEMPLATE_DIRS = [
        os.path.join(BASE_DIR, 'templates')
    ]


Create a folder in the root of your project called ```templates``` and add a new file named ```home.html```.
