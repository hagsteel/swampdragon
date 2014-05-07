from ..route_handler import BaseModelPublisherRouter
from .models import Company
from .serializers import CompanySerializer
from .dragon_django_test_case import DragonDjangoTestCase
from swampdragon import route_handler


class CompanyRouter(BaseModelPublisherRouter):
    model = Company
    route_name = 'test_company_router'
    serializer_class = CompanySerializer
    paginate_by = 3

    def get_query_set(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_object(self, **kwargs):
        return self.model.objects.get(**kwargs)


class TestPagination(DragonDjangoTestCase):
    def setUp(self):
        route_handler.register(CompanyRouter)

        for i in range(10):
            Company.objects.create(name='test co', comp_num=i)

    def test_paginate_result(self):
        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 1})
        page_1 = self.connection.get_last_message()['data']
        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 2})
        page_2 = self.connection.get_last_message()['data']
        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 3})
        page_3 = self.connection.get_last_message()['data']
        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 4})
        page_4 = self.connection.get_last_message()['data']

        self.assertListEqual(
            [p['id'] for p in page_1],
            [c['pk'] for c in Company.objects.all()[0:3].values('pk')]
        )
        self.assertListEqual(
            [p['id'] for p in page_2],
            [c['pk'] for c in Company.objects.all()[3:6].values('pk')]
        )
        self.assertListEqual(
            [p['id'] for p in page_3],
            [c['pk'] for c in Company.objects.all()[6:9].values('pk')]
        )
        self.assertListEqual(
            [p['id'] for p in page_4],
            [c['pk'] for c in Company.objects.all()[9:].values('pk')]
        )

    def test_paginator(self):
        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 1})
        page_1 = self.connection.get_last_message()['context']['client_context']
        self.assertTrue(page_1['page']['has_next'])
        self.assertFalse(page_1['page']['has_previous'])

        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 2})
        page_2 = self.connection.get_last_message()['context']['client_context']
        self.assertTrue(page_2['page']['has_next'])
        self.assertTrue(page_2['page']['has_previous'])

        self.connection.call_verb(CompanyRouter.route_name, 'get_list', **{'_page': 4})
        page_4 = self.connection.get_last_message()['context']['client_context']
        self.assertFalse(page_4['page']['has_next'])
        self.assertTrue(page_4['page']['has_previous'])
