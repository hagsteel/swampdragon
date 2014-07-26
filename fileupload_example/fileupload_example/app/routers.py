from datetime import datetime
from swampdragon import route_handler
from swampdragon.route_handler import BaseModelRouter
from .serializers import WithFileSerializer
from .models import WithFile


class WithFileRouter(BaseModelRouter):
    model = WithFile
    serializer_class = WithFileSerializer
    route_name = 'withfile-route'

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


route_handler.register(WithFileRouter)
