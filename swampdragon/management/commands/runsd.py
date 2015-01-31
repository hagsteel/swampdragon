from django.core.management.base import BaseCommand

from swampdragon.swampdragon_server import run_server


class Command(BaseCommand):
    def handle(self, *args, **options):
        host_port = None
        if args:
            host_port = args[0]
        run_server(host_port=host_port)
