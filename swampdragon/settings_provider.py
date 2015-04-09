from tornado.web import RequestHandler
from swampdragon.default_settings import SwampDragonSettings
from django.conf import settings as django_settings
from .same_origin import set_origin_cookie


def get_host():
    host = django_settings.DRAGON_URL
    if host.endswith('/'):
        return host[:-1]
    return host


class SettingsHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/javascript")
        set_origin_cookie(self)

    def get(self, *args, **kwargs):
        data = '''window.swampdragon_settings = {settings};
window.swampdragon_host = "{host}";
'''.format(**{
            'settings': SwampDragonSettings().to_dict(),
            'host': get_host()
        })
        self.write(data)
