from swampdragon.default_settings import SwampDragonSettings
from swampdragon.testing.dragon_testcase import DragonTestCase


class TestJavaScriptSettings(DragonTestCase):
    def test_user_settings(self):
        from django.conf import settings as django_settings
        django_settings.SWAMP_DRAGON = {
            'foo': 'bar',
        }
        settings = SwampDragonSettings()
        self.assertEqual(settings.to_dict()['foo'], 'bar')
