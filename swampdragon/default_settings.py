from django.conf import settings as django_settings


class SwampDragonSettings(object):
    def to_dict(self):
        settings = getattr(django_settings, 'SWAMP_DRAGON', {})
        settings['endpoints'] = []
        for connection, endpoint in django_settings.SOCKJS_CLASSES:
            settings['endpoints'].append(endpoint.replace('/', ''))
        return settings
