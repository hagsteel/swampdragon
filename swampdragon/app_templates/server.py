from django.conf import settings
from django.utils.importlib import import_module
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter
from swampdragon import discover_routes, load_field_deserializers
from swampdragon.settings_provider import SettingsHandler
import os
import sys


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<project>.settings")

if __name__ == '__main__':
    args = sys.argv
    HOST = '127.0.0.1'
    PORT = 9999

    if len(args) > 1:
        host_port = args[1]
        HOST = host_port.split(':')[0]
        PORT = host_port.split(':')[1]
    routers = []
    for sockjs_class in settings.SOCKJS_CLASSES:
        module_name, cls_name = sockjs_class[0].rsplit('.', 1)
        module = import_module(module_name)
        cls = getattr(module, cls_name)
        channel = sockjs_class[1]
        routers.append(SockJSRouter(cls, channel))
        print('Channel {}'.format(channel))

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
    print('Running SwampDragon on {}:{}'.format(HOST, PORT))
    try:
        iol = ioloop.IOLoop.instance()
        iol.start()
    except KeyboardInterrupt:
        # so you don't think you erred when ^C'ing out
        pass
