from rest_framework.viewsets import ModelViewSet

from planets.serializers import UniverseSerializer, PlanetSerializer
from planets.models import Universe, Planet


class UniverseViewSet(ModelViewSet):
    queryset = Universe.objects.all()
    serializer_class = UniverseSerializer


class PlanetViewSet(ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

