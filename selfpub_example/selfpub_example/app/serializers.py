from swampdragon.serializers.django_model_serializer import DjangoModelSerializer


class CompanyOwnerSerializer(DjangoModelSerializer):
    model = 'app.CompanyOwner'
    publish_fields = ['name', 'company_id']


class CompanySerializer(DjangoModelSerializer):
    model = 'app.Company'
    publish_fields = ['name', 'staff', 'companyowner']
    staff_serializer = 'app.StaffSerializer'
    companyowner_serializer = CompanyOwnerSerializer


class StaffSerializer(DjangoModelSerializer):
    model = 'app.Staff'
    publish_fields = ['name', 'documents', 'company_id']
    documents_serializer = 'app.DocumentSerializer'


class DocumentSerializer(DjangoModelSerializer):
    model = 'app.Document'
    publish_fields = ['title', 'content', 'staff']
    staff_serializer = StaffSerializer

    def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
        return [serializer.serialize(o, ignore_fields=['documents']) for o in obj.staff.all()]
