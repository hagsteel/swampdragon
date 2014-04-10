from swampdragon.serializers.django_model_serializer import DjangoModelSerializer


class WithFileSerializer(DjangoModelSerializer):
    model = 'app.WithFile'
    publish_fields = ['name', 'file', 'created', 'a_bool']
    update_fields = ['name', 'file', 'a_bool']
