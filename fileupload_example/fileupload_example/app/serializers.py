from swampdragon.serializers.model_serializer import ModelSerializer


class WithFileSerializer(ModelSerializer):
    class Meta:
        model = 'app.WithFile'
        publish_fields = ('name', 'file', 'created')
        update_fields = ('name', 'file')


class FileSerializer(ModelSerializer):
    class Meta:
        model = 'app.File'
        publish_fields = ('file')
        update_fields = ('file')


class MultiFileSerializer(ModelSerializer):
    files = FileSerializer

    class Meta:
        model = 'app.MultiFileModel'
        publish_fields = ('text', 'files')
        update_fields = ('text', 'files')
