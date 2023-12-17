from django.contrib import admin
from django.contrib.admin import ModelAdmin

from creatures.models import Creature


class CreatureAdmin(ModelAdmin):
    list_display = ('name', 'power')

    fields = [
        'name',
        'power',
        'icon',
        'planet',
    ]


admin.site.register(Creature, CreatureAdmin)