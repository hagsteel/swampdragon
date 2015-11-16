# Serializers

Serializers should reside in serializers.py inside your app: ```app/serializers.py```.

Use the ```ModelSerializer``` to serialize and deserialize your Django models.

    class FooSerializer(ModelSerializer):
        class Meta:
            model = 'app.FooModel'
            publish_fields = ('bar', )
            update_fields = ('bar', )


## Meta fields:

```model``` property can be either set to a Model or to a string (```model='app.Model'```).

```publish_fields``` is a list of fields on the model, to be published. If publish_fields is not defined, the entire model will be published.

```update_fields``` are fields that can be updated by submitting data to a router.


## Example

Serialize example: 

    foo = FooModel.objects.create(bar='hello world')
    serializer = FooSerializer(instance=foo)
    serializer.serialize()

Deserialize example:

    data = {'bar': 'hello world'}
    serializer = FooSerializer(data)
    foo = serializer.save()


## Custom field serialization 

Add a function ```serialize_<field_name>``` that returns either a dictionary or a primitive value.

    class FooSerializer(ModelSerializer):
        class Meta:
            model = Foo

        def serialize_full_name(self, obj):
            return '{} {}'.format(obj.first_name, obj.last_name)
            
The serialize_<field_name> takes argument: ```obj``` which is an instance of the model.

It is also possible to serialize a custom field with a related serializer.

    class FooSerializer(ModelSerializer):
        bar = BarSerializer
        
        def serialize_bar(self, obj, serializer):
            ...
            # In this instance the serializer would be an instance of a BarSerializer

If a property containing a serializer with the same name as the function (minus serialize_), that serializer will be included (see above code).

            
## Relationships

To include related data in a serializer, the related model need a serializer of it own.

    class FooSerializer(ModelSerializer):
        baz_set = 'BazSerializer'
    
        class Meta:
            model = 'app.FooModel'
            publish_fields = ('bar', 'baz_set')


    class BazSerializer(ModelSerializer):
        foo = FooSerializer
        
        class Meta:
            model = 'app.BazModel'
            publish_fields('foo', )

There are three ways to include a related serializer

Full path to serializer 


    from app.serializers import OtherSerializer
    
    class Serializer(ModelSerializer):
        related = OtherSerializer


\['serializer'\] (if the serializer is in the same .py file)


    class Serializer(ModelSerializer):
        related = 'OtherSerializer'


Serializing an instance of a FooModel will include the related BazModels, but the related BazModels will not contain the 
related FooModel and vice versa (to prevent infinite recursion).
