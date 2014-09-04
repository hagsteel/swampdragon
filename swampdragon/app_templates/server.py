import os
from swampdragon.swampdragon_server import run_server

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<project>.settings")

run_server()
