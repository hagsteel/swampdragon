from swampdragon.serializers.django_model_serializer import DjangoModelSerializer


class WithFileSerializer(DjangoModelSerializer):
    model = 'app.WithFile'
    publish_fields = ['name', 'file', 'created']
    update_fields = ['name', 'file']


class FileSerializer(DjangoModelSerializer):
    model = 'app.MultiFileModel'
    publish_fields = ['file']
    update_fields = ['file']


class MultiFileSerializer(DjangoModelSerializer):
    model = 'app.MultiFileModel'
    publish_fields = ['text', 'files']
    update_fields = ['text', 'files']
    files_serializer = FileSerializer
