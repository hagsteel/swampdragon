import django
from django.conf import settings
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter
from swampdragon import discover_routes, load_field_deserializers, VERSION
from swampdragon.settings_provider import SettingsHandler


def _output_server(host, port):
    """
    Print info about the current instance
    of SwampDragon
    """
    print('-------- SwampDragon ------')
    print('Running SwampDragon on {}:{}'.format(host, port))
    print('DRAGON_URL: {}'.format(settings.DRAGON_URL))
    print('Version {}'.format('.'.join([str(v) for v in VERSION])))
    print('Debug: {}'.format(settings.DEBUG))
    print('Quit the server with ctrl+c')
    print('---------------------------')


def run_server(host_port=None):
    if hasattr(django, 'setup'):
        django.setup()

    HOST = getattr(settings, 'SWAMP_DRAGON_HOST', '127.0.0.1')
    PORT = getattr(settings, 'SWAMP_DRAGON_PORT', 9999)

    if host_port is not None:
        HOST = host_port.split(':')[0]
        PORT = host_port.split(':')[1]
    routers = []

    if hasattr(settings, 'SOCKJS_CLASSES'):
        raise Exception('''
--------------
The SOCKJS_CLASSES setting has been removed in favour of SWAMP_DRAGON_CONNECTION

Update your settings and add SWAMP_DRAGON_CONNECTION.
--------------
        ''')

    module_name, cls_name = settings.SWAMP_DRAGON_CONNECTION[0].rsplit('.', 1)
    module = import_module(module_name)
    cls = getattr(module, cls_name)
    channel = settings.SWAMP_DRAGON_CONNECTION[1]
    routers.append(SockJSRouter(cls, channel))

    app_settings = {
        'debug': settings.DEBUG,
    }

    urls = discover_routes()
    for router in routers:
        urls += router.urls
    urls.append(('/settings.js$', SettingsHandler))

    load_field_deserializers()

    app = web.Application(urls, **app_settings)
    app.listen(PORT, address=HOST, no_keep_alive=False)

    _output_server(host=HOST, port=PORT)

    try:
        iol = ioloop.IOLoop.instance()
        iol.start()
    except KeyboardInterrupt:
        # so you don't think you erred when ^C'ing out
        pass
