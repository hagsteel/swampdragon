from django.conf import settings as django_settings


class SwampDragonSettings(object):
    def to_dict(self):
        settings = getattr(django_settings, 'SWAMP_DRAGON', {})
        settings['endpoint'] = django_settings.SWAMP_DRAGON_CONNECTION[1]
        return settings
