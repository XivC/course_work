from rest_framework.viewsets import ModelViewSet

from planets.models import Planet
from planets.models import Universe
from planets.serializers import PlanetSerializer
from planets.serializers import UniverseSerializer


class UniverseViewSet(ModelViewSet):
    queryset = Universe.objects.all()
    serializer_class = UniverseSerializer


class PlanetViewSet(ModelViewSet):
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
