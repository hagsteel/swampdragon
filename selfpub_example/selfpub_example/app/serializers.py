from swampdragon.serializers.model_serializer import ModelSerializer


class CompanyOwnerSerializer(ModelSerializer):
    class Meta:
        model = 'app.CompanyOwner'
        publish_fields = ['name', 'company_id']


class CompanySerializer(ModelSerializer):
    companyowner = CompanyOwnerSerializer
    staff = 'app.StaffSerializer'

    class Meta:
        model = 'app.Company'
        publish_fields = ['name', 'staff', 'companyowner']


class StaffSerializer(ModelSerializer):
    documents = 'app.DocumentSerializer'

    class Meta:
        model = 'app.Staff'
        publish_fields = ['name', 'documents', 'company_id']


class DocumentSerializer(ModelSerializer):
    staff = StaffSerializer

    class Meta:
        model = 'app.Document'
        publish_fields = ['title', 'content', 'staff']

    # def serialize_staff(self, obj=None, serializer=None):
    #     return [serializer(o).serialize for o in obj.staff.all()]
