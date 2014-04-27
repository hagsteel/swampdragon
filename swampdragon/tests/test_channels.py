from ..pubsub_providers.model_channel_builder import make_channels
from .serializers import CompanySerializer, DepartmentSerializer, LogoSerializer, StaffSerializer, DocumentSerializer
from ..pubsub_providers.channel_utils import channel_match_check
from .dragon_test_case import DragonTestCase


class TestChannelConstructor(DragonTestCase):
    def test_channels_from_company(self):
        property_filter = {'name__contains': 'foo'}
        channels = make_channels(CompanySerializer, [DepartmentSerializer, LogoSerializer], property_filter)
        expecpted = [
            'company|name__contains:foo',
            'department|company__name__contains:foo',
            'companylogo|company__name__contains:foo'
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_companylogo(self):
        property_filter = {'url': 'www.test.com'}
        channels = make_channels(LogoSerializer, property_filter=property_filter)
        expecpted = [
            'companylogo|url:www.test.com',
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_department(self):
        property_filter = {'name__contains': 'foo'}
        channels = make_channels(DepartmentSerializer, [StaffSerializer], property_filter)
        expecpted = [
            'department|name__contains:foo',
            'staff|department__name__contains:foo'
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_staff(self):
        property_filter = {'name__contains': 'foo'}
        channels = make_channels(StaffSerializer, [DocumentSerializer], property_filter)
        expecpted = [
            'staff|name__contains:foo',
            'document|staff__name__contains:foo'
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_document(self):
        property_filter = {'content__contains': 'foo'}
        channels = make_channels(DocumentSerializer, [StaffSerializer], property_filter)
        expecpted = [
            'document|content__contains:foo',
            'staff|document__content__contains:foo',
        ]
        self.assertListEqual(channels, expecpted)


class TestChannelUtils(DragonTestCase):
    def test_channel_match_check(self):
        channel = u'department|company__name__contains:foo'
        data = {'company_id': 1, 'id': 1, '_type': 'department', 'name': 'updated', 'staff': []}
        channel_match_check(channel, data)
