from swampdragon.serializers.django_model_serializer import DjangoModelSerializer


class WithFileSerializer(DjangoModelSerializer):
    model = 'app.WithFile'
    publish_fields = ['name', 'file']
    update_fields = ['name', 'file']
