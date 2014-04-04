from swampdragon import route_handler
from swampdragon.route_handler import BaseModelRouter
from .serializers import WithFileSerializer
from .models import WithFile


class WithFileRouter(BaseModelRouter):
    model = WithFile
    serializer_class = WithFileSerializer
    route_name = 'withfile-route'
    # valid_verbs = ['chat', 'subscribe']


route_handler.register(WithFileRouter)
