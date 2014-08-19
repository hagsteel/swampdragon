from django.db import models
from .dragon_test_case import DragonTestCase
from ..serializers.model_serializer import ModelSerializer
from ..serializers import serializer_tools
from swampdragon.tests.models import SDModel


class ReverseM2M(SDModel):
    number = models.IntegerField()


class M2M(SDModel):
    name = models.CharField(max_length=10)
    many = models.ManyToManyField(ReverseM2M)


class ReverseFk(SDModel):
    name = models.CharField(max_length=10)


class Fk(SDModel):
    number = models.IntegerField()
    reverse_fk = models.ForeignKey(ReverseFk)


class ReverseM2MSerializer(ModelSerializer):
    m2m_set = 'M2MSerializer'

    class Meta:
        model = ReverseM2M
        publish_fields = ('number', 'm2m_set')


class ReverseO2O(SDModel):
    bar = models.CharField(max_length=100)


class O2O(SDModel):
    foo = models.CharField(max_length=100)
    reverse_o2o = models.OneToOneField(ReverseO2O)


class M2MSerializer(ModelSerializer):
    many = ReverseM2MSerializer

    class Meta:
        model = M2M


class FKSerializer(ModelSerializer):
    reverse_fk = 'ReverseFKSerializer'

    class Meta:
        model = Fk
        publish_fields = ('reverse_fk', )


class ReverseFKSerializer(ModelSerializer):
    fk_set = FKSerializer

    class Meta:
        model = ReverseFk
        publish_fields = ('fk_set', )


class O2OSerializer(ModelSerializer):
    reverse_o2o = 'ReverseO2OSerializer'

    class Meta:
        model = O2O


class ReverseO2OSerializer(ModelSerializer):
    o2o = O2OSerializer

    class Meta:
        model = ReverseO2O
        fields = ('o2o')


class TestSerializerTools(DragonTestCase):
    def test_m2m(self):
        reverse_m2m = ReverseM2M.objects.create(number=12)
        m2m = M2M.objects.create(name='test')
        m2m.many.add(reverse_m2m)
        mapping = serializer_tools.get_id_mappings(M2MSerializer(instance=m2m))
        self.assertEqual(list(mapping['many']), [reverse_m2m.pk])

    def test_reverse_m2m(self):
        reverse_m2m = ReverseM2M.objects.create(number=12)
        m2m = M2M.objects.create(name='test')
        m2m.many.add(reverse_m2m)
        mapping = serializer_tools.get_id_mappings(ReverseM2MSerializer(instance=reverse_m2m))
        self.assertEqual(list(mapping['m2m_set']), [m2m.pk])

    def test_fk(self):
        reverse_fk = ReverseFk.objects.create(name='test')
        fk = Fk.objects.create(number=99, reverse_fk=reverse_fk)
        mapping = serializer_tools.get_id_mappings(FKSerializer(instance=fk))
        self.assertEqual(mapping['reverse_fk'], reverse_fk.pk)

    def test_reverse_fk(self):
        reverse_fk = ReverseFk.objects.create(name='test')
        fk = Fk.objects.create(number=99, reverse_fk=reverse_fk)
        mapping = serializer_tools.get_id_mappings(ReverseFKSerializer(instance=reverse_fk))
        self.assertEqual(list(mapping['fk_set']), [fk.pk])

    def test_one2one(self):
        ro2o = ReverseO2O.objects.create(bar='another test')
        o2o = O2O.objects.create(foo='test', reverse_o2o=ro2o)
        mapping = serializer_tools.get_id_mappings(O2OSerializer(instance=o2o))
        self.assertEqual(mapping['reverse_o2o'], ro2o.pk)

    def test_reverse_one2one(self):
        ro2o = ReverseO2O.objects.create(bar='another test')
        o2o = O2O.objects.create(foo='test', reverse_o2o=ro2o)
        mapping = serializer_tools.get_id_mappings(ReverseO2OSerializer(instance=ro2o))
        self.assertEqual(mapping['o2o'], o2o.pk)
