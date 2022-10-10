from rest_framework.viewsets import ModelViewSet

from ads.models import Location
from ads.serializer import LocatSerializer


class LocatViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocatSerializer
