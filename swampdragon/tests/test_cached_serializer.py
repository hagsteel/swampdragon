from .dragon_django_test_case import DragonDjangoTestCase
from .models import CacheFooModel, CacheBarModel, FooModel, BarModel


class SerializerExtraDataTest(DragonDjangoTestCase):
    '''
    Test caching of serializer data
    '''
    def test_lots_of_data(self):
        model_count = 1000

        # foo = FooModel.objects.create(test_field_a='hello', test_field_b='world')
        # for i in range(model_count):
        #     bar = BarModel.objects.create(number=i, foo=foo)
        #
        # for bar in BarModel.objects.all():
        #     bar.serialize()

        foo = CacheFooModel.objects.create(test_field_a='hello', test_field_b='world')
        for i in range(model_count):
            bar = CacheBarModel.objects.create(number=i, foo=foo)

        for bar in CacheBarModel.objects.all():
            bar.serialize()
