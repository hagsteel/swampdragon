#  Code from https://github.com/peterbe/django-sockjs-tornado
#  Tweaked to handle multiple routes
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter
from swampdragon import discover_routes, load_field_deserializers


class Command(BaseCommand):
    # option_list = BaseCommand.option_list + (
    #     make_option(
    #         '--host',
    #         action='store',
    #         dest='host',
    #         default='127.0.0.1',
    #         help='Host'),
    #     make_option(
    #         '--port',
    #         action='store',
    #         dest='port',
    #         default=getattr(settings, 'SOCKJS_PORT', 9999),
    #         help='What port number to run the socket server on'),
    #     make_option(
    #         '--no-keep-alive',
    #         action='store_true',
    #         dest='no_keep_alive',
    #         default=False,
    #         help='Set no_keep_alive on the connection if your server needs it')
    # )

    def handle(self, *args, **kwargs):
        HOST = '127.0.0.1'
        PORT = 9999

        if args:
            host_port = args[0]
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

        load_field_deserializers()

        app = web.Application(urls, **app_settings)
        app.listen(PORT, address=HOST, no_keep_alive=False)
        print('Running sock app on {}:{}'.format(HOST, PORT))
        try:
            iol = ioloop.IOLoop.instance()
            # ioloop.IOLoop.set_blocking_log_threshold(iol, 1)
            iol.start()
        except KeyboardInterrupt:
            # so you don't think you erred when ^C'ing out
            pass
