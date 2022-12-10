from rest_framework.routers import DefaultRouter

from creatures.views import CreatureViewSet

router = DefaultRouter()
router.register(r'creatures', CreatureViewSet)

urlpatterns = router.urls
