# Serializers #

Serializers should reside in serializers.py inside your app: `app/serializers.py`.

Use the `ModelSerializer` to serialize and deserialize your Django models.

```python
from swampdragon.serializers.model_serializer import ModelSerializer

class FooSerializer(ModelSerializer):
    class Meta:
        model = 'app.FooModel'
        publish_fields = ('bar', )
        update_fields = ('bar', )
```


## Meta fields ##


### model ###

Sets the related model. The value can be either set to a Model class or to a string.

```python
model = 'app.Model'
```

```python
model = FooModel
```


### publish_fields ###

Sets a list of fields on the model, to be published. If `publish_fields` is not defined, the entire model will be published.

```python
publish_fields = ('bar', )
```

### update_fields ###
Sets the fields that can be updated by submitting data to a router.

```python
update_fields = ('bar', )
```


## Example ##


### Serialize ###

```python
foo = FooModel.objects.create(bar='hello world')
serializer = FooSerializer(instance=foo)
serializer.serialize()
```


### Deserialize ###

```python
data = {'bar': 'hello world'}
serializer = FooSerializer(data)
foo = serializer.save()
```


## Custom field serialization ##

Add a function `serialize_<field_name>` that returns either a dictionary or a primitive value.

```python
from swampdragon.serializers.model_serializer import ModelSerializer


class FooSerializer(ModelSerializer):
    class Meta:
        model = Foo

    def serialize_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)
```

The `serialize_<field_name>` takes argument: `obj` which is an instance of the model.

It is also possible to serialize a custom field with a related serializer.

```python
from swampdragon.serializers.model_serializer import ModelSerializer


class FooSerializer(ModelSerializer):
    bar = BarSerializer

    def serialize_bar(self, obj, serializer):
        ...
        # In this instance the serializer would be an instance of a BarSerializer
```
If a property containing a serializer with the same name as the function (minus serialize_), that serializer will be included (see above code).


## Relationships ##

To include related data in a serializer, the related model need a serializer of it own.


### Example ###

```python
from swampdragon.serializers.model_serializer import ModelSerializer


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
```


### Defining the related field ###

There are three ways to include a related serializer:

By referencing the serializer class.

```python
from app.serializers import OtherSerializer

class Serializer(ModelSerializer):
    related_fieldname = OtherSerializer
```

By referencing the full path as string. `['app'].['serializer']`

```python
class Serializer(ModelSerializer):
    related_fieldname = 'app.OtherSerializer'
```

Or by defining the serializer name, if its defined in the same `serializers.py` file.

```python
class Serializer(ModelSerializer):
    related_fieldname = 'OtherSerializer'
```

Serializing an instance of a `FooModel` will include the related `BazModels`, but the related `BazModels` will not contain the
related `FooModel` and vice versa (to prevent infinite recursion).

In order to get updates from related models to the parent router, look at [include_related](/documentation/routers/index#include_related).
