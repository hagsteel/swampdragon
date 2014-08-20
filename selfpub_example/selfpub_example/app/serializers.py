from swampdragon.serializers.model_serializer import ModelSerializer


class CompanyOwnerSerializer(ModelSerializer):
    class Meta:
        model = 'app.CompanyOwner'


class CompanySerializer(ModelSerializer):
    companyowner = CompanyOwnerSerializer
    staff = 'app.StaffSerializer'

    class Meta:
        model = 'app.Company'
        publish_fields = ('name', 'staff', 'companyowner')
        update_fields = ('name', )


class StaffSerializer(ModelSerializer):
    documents = 'app.DocumentSerializer'

    class Meta:
        model = 'app.Staff'
        publish_fields = ('name', 'documents', 'company')


class DocumentSerializer(ModelSerializer):
    class Meta:
        model = 'app.Document'
        publish_fields = ('title', 'content', 'staff')
