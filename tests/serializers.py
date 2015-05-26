from swampdragon.serializers.model_serializer import ModelSerializer


class FooSelfPubSerializer(ModelSerializer):
    bars = 'BarSelfPubSerializer'

    class Meta:
        model = 'tests.FooSelfPub'
        publish_fields = ('name', 'number', 'bars')


class BarSelfPubSerializer(ModelSerializer):
    foo = FooSelfPubSerializer

    class Meta:
        model = 'tests.BarSelfPub'
        publish_fields = ('date', 'foo', 'id')


class BoolSelfPubSerializer(ModelSerializer):
    class Meta:
        model = 'tests.BoolSelfPub'
        publish_fields = ('bool', )
