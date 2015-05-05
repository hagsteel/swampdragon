from rest_framework.serializers import ModelSerializer as DRFModelSerializer
from tests.models import DRFModel


class DRFSerializer(DRFModelSerializer):
    class Meta:
        model = DRFModel
