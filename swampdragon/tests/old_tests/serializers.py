from ..serializers.cached_serializer import CacheModelSerializer
from ..serializers.model_serializer import ModelSerializer

################################
# Old school serializers
################################


class DepartmentSerializer(ModelSerializer):
    staff = 'tests.StaffSerializer'

    class Meta:
        model = 'tests.Department'
        publish_fields = ['name', 'company_id', 'staff']
        update_fields = ['name']

    def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
        return [StaffSerializer().serialize(s, ignore_fields=['departments']) for s in obj.staff.all()]


class StaffSerializer(ModelSerializer):
    documents = 'tests.DocumentSerializer'

    class Meta:
        model = 'tests.Staff'
        publish_fields = ('name', 'documents')
        update_fields = ('name', )
        documents_serializer = 'tests.DocumentSerializer'


class LogoSerializer(ModelSerializer):
    class Meta:
        model = 'tests.CompanyLogo'
        publish_fields = ['url']


class CompanySerializer(ModelSerializer):
    departments = DepartmentSerializer
    logo = LogoSerializer

    class Meta:
        model = 'tests.Company'
        publish_fields = ['name', 'comp_num', 'departments', 'logo', 'custom_field']
        update_fields = ['name', 'comp_num']

    def serialize_custom_field(self, obj=None, serializer=None, ignore_fields=[]):
        return 'custom field'


class DocumentSerializer(ModelSerializer):
    staff = StaffSerializer

    class Meta:
        model = 'tests.Document'
        publish_fields = ['name', 'content', 'staff']
        staff_serializer = StaffSerializer

    # def serialize_staff(self, obj=None, serializer=None, ignore_fields=[]):
    #     return [serializer.serialize(o, ignore_fields=['documents']) for o in obj.staff.all()]


################################
# New serializeres
################################
class FooSerializer(ModelSerializer):
    bars = 'tests.BarSerializer'

    class Meta:
        publish_fields = ('test_field_a', 'bars')
        update_fields = ('test_field_a', 'test_field_b', 'bars')
        model = 'tests.FooModel'


class BarSerializer(ModelSerializer):
    foo = FooSerializer

    class Meta:
        model = 'tests.BarModel'
        update_fields = ('number', 'foo')
        publish_fields = ('number', 'foo')


class BazSerializer(ModelSerializer):
    bar = BarSerializer

    class Meta:
        model = 'tests.BazModel'
        update_fields = ('name', 'bar')
        publish_fields = ('name', 'bar')


class QuxSerializer(ModelSerializer):
    foos = FooSerializer

    class Meta:
        model = 'tests.QuxModel'
        publish_fields = ('value', 'foos')
        update_fields = ('value', 'foos')


class CacheFooSerializer(CacheModelSerializer):
    bars = 'tests.CacheBarSerializer'

    class Meta:
        model = 'tests.CacheFooModel'
        publish_fields = ('test_field_a', 'bars')
        update_fields = ('test_field_a', 'test_field_b', 'bars')


class CacheBarSerializer(CacheModelSerializer):
    foo = CacheFooSerializer

    class Meta:
        model = 'tests.CacheBarModel'
        update_fields = ('number', 'foo')
        publish_fields = ('number', 'foo')
