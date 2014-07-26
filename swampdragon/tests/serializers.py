from ..serializers.django_model_serializer import DjangoModelSerializer


class DepartmentSerializer(DjangoModelSerializer):
    model = 'tests.Department'
    publish_fields = ['name', 'company_id', 'staff']
    update_fields = ['name']

    def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
        return [StaffSerializer().serialize(s, ignore_fields=['departments']) for s in obj.staff.all()]


class StaffSerializer(DjangoModelSerializer):
    model = 'tests.Staff'
    publish_fields = ['name', 'department.company.id', 'documents']
    update_fields = ['name']
    documents_serializer = 'tests.DocumentSerializer'

    def serialize_documents(self, obj=None, serializer=None):
        return [serializer.serialize(d, ignore_fields=['staff']) for d in obj.documents.all()]


class LogoSerializer(DjangoModelSerializer):
    model = 'tests.CompanyLogo'
    publish_fields = ['url']


class CompanySerializer(DjangoModelSerializer):
    model = 'tests.Company'
    publish_fields = ['name', 'comp_num', 'departments', 'logo', 'custom_field']
    update_fields = ['name', 'comp_num', 'departments']
    departments_serializer = DepartmentSerializer
    logo_serializer = LogoSerializer

    def serialize_custom_field(self, obj=None, serializer=None, ignore_fields=[]):
        return 'custom field'


class DocumentSerializer(DjangoModelSerializer):
    model = 'tests.Document'
    publish_fields = ['name', 'content', 'staff']
    staff_serializer = StaffSerializer

    def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
        return [serializer.serialize(o, ignore_fields=['documents']) for o in obj.staff.all()]
