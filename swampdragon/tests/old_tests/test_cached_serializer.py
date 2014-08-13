# from django.utils.unittest.case import skip
# from .dragon_django_test_case import DragonDjangoTestCase
# from .models import CacheFooModel, CacheBarModel, FooModel, BarModel
#
#
# class SerializerExtraDataTest(DragonDjangoTestCase):
#     '''
#     Test caching of serializer data.
#     Serializing foo should result in no queries
#     '''
#     def test_lots_of_data(self):
#         model_count = 10
#
#         foo = FooModel.objects.create(test_field_a='hello', test_field_b='world')
#         for i in range(model_count):
#             bar = BarModel.objects.create(number=i, foo=foo)
#
#         for bar in BarModel.objects.all():
#             # with self.assertNumQueries(11):
#             data = foo.serialize()
#
#         foo = CacheFooModel.objects.create(test_field_a='hello', test_field_b='world')
#         for i in range(model_count):
#             bar = CacheBarModel.objects.create(number=i, foo=foo)
#
#         for bar in CacheBarModel.objects.all():
#             with self.assertNumQueries(0):
#                 data = foo.serialize()
#                 self.assertGreater(len(data['bars']), 0)
