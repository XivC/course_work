from django.urls import include
from django.urls import path
from rest_framework_nested import routers

from affects.views import CreatureEffectRuleViewSet
from affects.views import EffectViewSet
from affects.views import PlanetEffectRuleViewSet
from affects.views import WeaponViewSet

weapon_router = routers.SimpleRouter()
weapon_router.register('weapons', WeaponViewSet)

effect_router = routers.SimpleRouter()
effect_router.register('effects', EffectViewSet)

rule_router = routers.NestedSimpleRouter(effect_router, 'effects', lookup='effect')
rule_router.register('planets-rules', PlanetEffectRuleViewSet)
rule_router.register('creatures-rules', CreatureEffectRuleViewSet)

urlpatterns = [
    path('', include(effect_router.urls)),
    path('', include(rule_router.urls)),
]
