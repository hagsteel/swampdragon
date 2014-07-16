from swampdragon import route_handler
from swampdragon.route_handler import BaseModelPublisherRouter
from .serializers import CompanySerializer, StaffSerializer, DocumentSerializer, CompanyOwnerSerializer
from .models import Company


class CompanyRouter(BaseModelPublisherRouter):
    serializer_class = CompanySerializer
    model = Company
    route_name = 'company-route'
    include_related = [StaffSerializer, DocumentSerializer, CompanyOwnerSerializer]

    def get_query_set(self, **kwargs):
        return self.model.objects.all()

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['pk'])


route_handler.register(CompanyRouter)
