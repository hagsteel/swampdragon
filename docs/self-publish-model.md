# Self publishing models

Self publishing models will update as they are saved.
Include the ```SelfPublishModel``` mixin and assign a serializer to ```serializer_class```.

    from django.db import models
    from swampdragon.models import SelfPublishModel
    
    class Foo(SelfPublishModel, models.Model):
        text = models.CharField(max_length=100)
        serializer_class = FooSerializer


Every time the model is updated it will publish the changes to all subscribers.
