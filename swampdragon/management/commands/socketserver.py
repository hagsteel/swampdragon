#  Code from https://github.com/peterbe/django-sockjs-tornado
#  Tweaked to handle multiple routes
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.importlib import import_module
from tornado import web, ioloop
from sockjs.tornado import SockJSRouter
from swampdragon import autodiscover_routes


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--host',
            action='store',
            dest='host',
            default='127.0.0.1',
            help='Host'),
        make_option(
            '--port',
            action='store',
            dest='port',
            default=getattr(settings, 'SOCKJS_PORT', 9999),
            help='What port number to run the socket server on'),
        make_option(
            '--no-keep-alive',
            action='store_true',
            dest='no_keep_alive',
            default=False,
            help='Set no_keep_alive on the connection if your server needs it')
    )

    def handle(self, **options):
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

        HOST = options['host']
        PORT = int(options['port'])
        urls = []
        for router in routers:
            urls += router.urls

        app = web.Application(urls, **app_settings)
        app.listen(PORT, address=HOST, no_keep_alive=options['no_keep_alive'])
        print('Running sock app on {}:{}'.format(HOST, PORT))
        try:
            autodiscover_routes()
            iol = ioloop.IOLoop.instance()
            # ioloop.IOLoop.set_blocking_log_threshold(iol, 1)
            iol.start()
        except KeyboardInterrupt:
            # so you don't think you errored when ^C'ing out
            pass
