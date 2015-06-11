from django.core.management.base import BaseCommand

from swampdragon.swampdragon_server import run_server


class Command(BaseCommand):
    args = '<host_port>'
    
    def handle(self, *args, **options):
        host_port = None
        if args:
            host_port = args[0]
        run_server(host_port=host_port)
        
    """
    # This is the preferred way to implement positional arguments in Django 1.8, but breaks pre 1.8
    def add_arguments(self, parser):
        parser.add_argument('host_port', nargs='?', default=None, type=str)

    def handle(self, *args, **options):
        run_server(host_port=options['host_port'])
    """
