from django.contrib import admin
from django.contrib.admin import ModelAdmin

from affects.models import Weapon, Effect, CreatureEffectRule, PlanetEffectRule


class WeaponAdmin(ModelAdmin):
    list_display = ('name', 'power')

    fields = [
        'name',
        'power',
        'icon',
    ]


class EffectAdmin(ModelAdmin):
    list_display = ('name', 'power_affect')

    fields = [
        'name',
        'power_affect',
    ]


class CreatureEffectRuleAdmin(ModelAdmin):
    list_display = ('creature_from', 'creature_to', 'effect', 'is_to_ally')

    fields = [
        'creature_from',
        'creature_to',
        'effect',

    ]


class PlanetEffectRuleAdmin(ModelAdmin):
    list_display = ('planet', 'creature_to', 'effect')

    fields = [
        'planet',
        'creature_to',
        'effect',

    ]


admin.site.register(Weapon, WeaponAdmin)
admin.site.register(Effect, EffectAdmin)
admin.site.register(CreatureEffectRule, CreatureEffectRule)
admin.site.register(PlanetEffectRule, PlanetEffectRuleAdmin)
