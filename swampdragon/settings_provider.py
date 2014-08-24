from tornado.web import RequestHandler
from swampdragon.default_settings import SwampDragonSettings


class SettingsHandler(RequestHandler):

    def head(self, *args, **kwargs):
        self.set_header("Content-Type", "text/javascript; charset=UTF-8")

    def get(self, *args, **kwargs):
        data = '''window.swampdragon_settings = {settings};
window.swamp_dargon_host = "{protocol}://{host}";
        '''.format(**{
            'settings': SwampDragonSettings().to_dict(),
            'host': self.request.headers['Host'],
            'protocol': self.request.protocol,
        })
        self.write(data)
