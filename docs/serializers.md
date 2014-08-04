# Serializers

Serializers should reside in app/serializers.py

Use the ```ModelSerializer``` to serialize and deserialize your Django models.

## Meta fields:

```model``` property can be either set to a Model or to a string (app.Model).

```publish_fields``` is a list of fields on the model, to be published.

```update_fields``` are fields that can be updated by submitting data to a router.



Model

    class FooModel(models.Model):
        bar = models.CharField(max_length=100)
        

Serializer

    class FooSerializer(ModelSerializer):
        class Meta:
            model = 'app.FooModel'
            publish_fields = ('bar', )
            update_fields = ('bar', )
            

### Examples
 
#### Serialize

    foo = FooModel.objects.create(bar='hello world')
    serializer = FooSerializer(instance=foo)
    serializer.serialize()
    
#### Deserialize

    data = {'bar': 'hello world'}
    serializer = FooSerializer(data)
    foo = serializer.save()
    
    
## Custom field serialization 

To serialize a custom field include the field in the ```publish_fields``` list.
Add a function ```serialize_<field_name>``` that returns either a dictionary or a primitive value.

#### Example

    class FooSerializer(ModelSerializer):
        def custom_field(obj, serializer):
            return {'mesage': 'this is a custom field'}
    
        class Meta:
            model = 'app.FooModel'
            publish_fields = ('bar', 'custom_field')
            update_fields = ('bar', )


## Relationships

To include related data in a serializer the related model need a serializer of it own.

    class FooSerializer(ModelSerializer):
        baz_set = 'app.BazSerializer'
    
        class Meta:
            model = 'app.FooModel'
            publish_fields = ('bar', 'baz_set')


    class BazSerializer(ModelSerializer):
        foo = FooSerializer
        
        class Meta:
            model = 'app.BazModel'
            publish_fields('foo', )
            
    
Serializing an instance of a FooModel will include related BazModels, but the related BazModels will not contain the 
related FooModel and vice versa (to prevent infinite recursion)


