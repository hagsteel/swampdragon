Swamp Dragon
============

# UNDER DEVELOPMENT DON'T USE THIS YET

Swamp Dragon is a pub/sub solution running on top of Tornado, and is compatible with Django models.
It allows data to be published to channels via routers and does all the heavy lifting.


# Important
**Note**: As Django models are blocking, long queries will prevent other requests to come through.

**Note**: Currently it's heavily tied to Django

**Note**: All serializers needs to reside in serializers.py


#TODO
*  Important note about related serializers
*  Write documentation
*  Add instructions for swampDragon.call = function(verb, route, channel, args, callbackName)
*  Add instructions on self publishing models
*  term_match_check: make sure compared values are of the same type
*  Filter case sensitivity
*  File upload


# Serializer

    def serialize_<field>(obj, serializer, ignore_fields)

In a situation with a m2m relationship, where there is a serializer for both models, one of the models
need to set the ignore_fields=['<field name>'] or it will result in infinite recursion.

## Fields

    *  model
    *  publish_fields
    *  update_fields
    *  channel_filter_fields
    *  include_related
    *  <field_name>_serializer

### ```model```
The model field on the serializer can be set to either the model, or a string representation of the model:
'app.Model'.

### ```publish_fields```
These are the fields that are published to all subscribers.


### ```update_fields```
The fields that can be updated by the client.

### ```channel_filter_fields```
A channel match is done by checking the publish fields against available channels.
In some cases, a channel filter needs to include a field that is not editable, or visible to the end user,
i.e: a foreign key relationship, a user id etc.

### ```Include related```

Publishing based related data is done by setting ```include_related``` on the serializer.
Include related is a tuple containing the related serializer and the property for the serializer.

    class CompanySerializer(DjangoModelSerializer):
        model = 'app.Model'
        include_related = [
            (BarSerializer, 'foo.id')
        ]


In the above example, the Foo serializer will include all the related Bar data, where the foo.id matches the
instance of the Foo serializer.


### ```<field_name>_serializer```

Specify a serializer for a field


# Self publishing models

A model can be self publishing, meaning every time the model is saved it's also published.

In case a model should not publish until properly constructed:
**Note**  ```with Document(name='test doc') as document:``` will actually call save() on the document instance

    with Document(name='test doc') as document:
        document.staff.add(staff_a)
        document.staff.add(staff_b)


# JavaScript implementation

## Data mapper

To bind the data use the dataMapper together with the channelMapper to accurately map the data to the correct channel.

    dataMapper.mapDataSetup $scope, 'parents', [
        {type: 'child', map_to: 'parent', map_by: 'parent_id', map_from: 'children'},
        {type: 'sub_child', map_to: 'child', map_by: 'child_id', map_from: 'subchildren'}
    ]

In this scenario we are mapping the child model to the parent model via the parent id, to the parent's children.
In this case children is a collection of ```child``` models

We are also mapping the sub_child model tot he child model, via the child_id, and subchildren is a collection
on the child model.
