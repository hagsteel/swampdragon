from django.core.management.base import BaseCommand

from swampdragon.swampdragon_server import run_server


class Command(BaseCommand):

    def handle(self, *args, **options):
        run_server()
