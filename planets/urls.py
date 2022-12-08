from rest_framework.routers import DefaultRouter

from planets.views import PlanetViewSet
from planets.views import UniverseViewSet

router = DefaultRouter()
router.register(r'universes', UniverseViewSet)
router.register(r'planets', PlanetViewSet)

urlpatterns = router.urls
