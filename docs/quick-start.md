# Quick start

Install Swamp Dragon: [see installation instructions](/documentation/installation/). 

Open a terminal and start redis with the following command:

    redis-server

To start a new project run 

    dragon-admin startproject <project name>

Create the initial app

    django-admin.py startapp <module name>
    
    
Add a model to your app

    from django.db import models
    from swampdragon.models import SelfPublishModel
    from .serializers import FooSerializer
    
    
    class Foo(SelfPublishModel, models.Model):
        serializer_class = FooSerializer
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
    from swampdragon.route_handler import ModelPublisherRouter
    from .serializers import FooSerializer
    from .models import Foo
    
    
    class FooRouter(ModelPublisherRouter):
        serializer_class = FooSerializer
        model = Foo
        route_name = 'foo'
    
        def get_object(self, **kwargs):
            return self.model.objects.get(pk=kwargs['pk'])
    
        def get_query_set(self, **kwargs):
            return self.model.all()
    
    
    route_handler.register(FooRouter)

A demo project with templates and static files setup can be found on [
Github](https://github.com/jonashagstedt/swampdragon)
