from swampdragon import route_handler
from swampdragon.route_handler import BaseModelRouter
from .serializers import WithFileSerializer, MultiFileSerializer
from .models import WithFile, MultiFileModel


class WithFileRouter(BaseModelRouter):
    model = WithFile
    serializer_class = WithFileSerializer
    route_name = 'withfile-route'

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


class MultiFileRouter(BaseModelRouter):
    model = MultiFileModel
    serializer_class = MultiFileSerializer
    route_name = 'multifile-route'

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all()


route_handler.register(WithFileRouter)
route_handler.register(MultiFileRouter)
