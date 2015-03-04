# Field deserializers #

Create a file and name it `field_deserializers.py`.
This file needs to reside inside an app `app/field_deserializers.py`.

Extend `BaseFieldDeserializer`

The following example will append the word 'foo' to every CharField

```python
from swampdragon.serializers.field_deserializers import BaseFieldDeserializer
from swampdragon.serializers.field_deserializers import register_field_deserializer


class FooDeserializer(BaseFieldDeserializer):
    def __call__(self, model_instance, key, val):
        deserialized_val = 'foo {}'.format(val)
        setattr(model_instance, key, deserialized_val)


register_field_deserializer('CharField', FileDeserializer)
```

Register the deserializer by adding a string representation of the field type along with the serializer.

```python
register_field_deserializer('CharField', FileDeserializer)
```
