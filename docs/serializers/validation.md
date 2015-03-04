# Validation #

It's possible to add custom validation to fields.

Add a function `validate_<field name>`

```python
def validate_text(self, val):
    if val == 'foo':
        raise ModelValidationError({'text': ['text error']})
```


## Raising an error ##

If a field isn't valid, raise a `ModelValidationError`.
The ModelValidationError takes a dictionary and a list of validation errors {'<field name>': [<list of errors>]}


## Example ##

```python
from swampdragon.serializers.model_serializer import ModelSerializer


class FooSerializer(ModelSerializer):

    def validate_text(self, val):
        if val == 'foo':
            raise ModelValidationError({'text': ['text error']})

    class Meta:
        model = 'app.FooModel'
        publish_fields = ('text', )

```
