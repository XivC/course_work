from django.urls import include
from django.urls import path
from rest_framework import routers

from adventures.views import AdventureViewSet

router = routers.SimpleRouter()
router.register('adventures', AdventureViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
