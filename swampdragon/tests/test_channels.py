from django_webtest import WebTest
from ..pubsub_providers.model_channel_builder import make_channels
from .serializers import CompanySerializer, DepartmentSerializer, LogoSerializer, StaffSerializer, DocumentSerializer
from ..pubsub_providers.channel_utils import channel_match_check


class TestChannelConstructor(WebTest):
    def test_channels_from_company(self):
        kwargs = {'name__contains': 'foo'}
        channels = make_channels(CompanySerializer, [DepartmentSerializer, LogoSerializer], **kwargs)
        expecpted = [
            'company|name__contains:foo',
            'department|company__name__contains:foo',
            'companylogo|company__name__contains:foo'
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_companylogo(self):
        kwargs = {'url': 'www.test.com'}
        channels = make_channels(LogoSerializer, **kwargs)
        expecpted = [
            'companylogo|url:www.test.com',
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_department(self):
        kwargs = {'name__contains': 'foo'}
        channels = make_channels(DepartmentSerializer, [StaffSerializer], **kwargs)
        expecpted = [
            'department|name__contains:foo',
            'staff|department__name__contains:foo'
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_staff(self):
        kwargs = {'name__contains': 'foo'}
        channels = make_channels(StaffSerializer, [DocumentSerializer], **kwargs)
        expecpted = [
            'staff|name__contains:foo',
            'document|staff__name__contains:foo'
        ]
        self.assertListEqual(channels, expecpted)

    def test_channels_from_document(self):
        kwargs = {'content__contains': 'foo'}
        channels = make_channels(DocumentSerializer, [StaffSerializer], **kwargs)
        expecpted = [
            'document|content__contains:foo',
            'staff|document__content__contains:foo',
        ]
        self.assertListEqual(channels, expecpted)


class TestChannelUtils(WebTest):
    def test_channel_match_check(self):
        channel = u'department|company__name__contains:foo'
        data = {'company_id': 1, 'id': 1, '_type': 'department', 'name': 'updated', 'staff': []}
        channel_match_check(channel, data)
